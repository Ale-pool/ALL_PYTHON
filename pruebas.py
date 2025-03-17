def extraer_info_general(self):
    info_general = {}
    try:
        info = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", info)
        time.sleep(2)
        info = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/div/div/div[2]/div[2]/div/div[1]/a"))
        )
        info.click()
    except TimeoutException:
        print(f"No se encontró información para el NIT: {self.nit}")
        return [np.nan] * 15 + [self.nit]
    except NoSuchElementException:
        print(f"No se encontró información para el NIT: {self.nit}")
        return [np.nan] * 15 + [self.nit]

    # Extraer información general
    try:
        data = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/div/div[2]/div[1]/div"))
        )                                              
        info_general = data.text
        print(info_general)

        info_lines = info_general.split('\n')  # Separar la información por líneas
        data_dic = {}
        for i in range(0, len(info_lines), 2):   # Recorrer la información general
            key = info_lines[i].strip()
            value = info_lines[i+1].strip() if i+ 1 < len(info_lines) else ""
            if key in "Identificación":
                value_split = value.split()
                value = value.split()[1]  if len(value_split) > 1 else ""
            data_dic[key] = value
        
        # Obtener la información de la actividad económica
        actividad = self.driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div[1]/div/div[1]/div[2]/a/span")
        actividad.click()
        actingo = self.driver.find_element(By.ID, "detail-tabs-tabpane-pestana_economica")
        actingo_text = actingo.text
        print(actingo_text)

        actividad_numeros = ''.join(filter(str.isdigit, actingo_text))
        data_dic["Actividad Económica"] = actividad_numeros
        columnas = ['Identificación', 'Categoria de la Matrícula','Tipo de Sociedad','Tipo Organización','Cámara de Comercio',
                    'Número de Matrícula','Fecha de Matrícula','Fecha de Vigencia','Estado de la matrícula',
                    'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social','Extinción de Dominio', 'Actividad Económica']
        valores = [data_dic.get(col, np.nan) for col in columnas]  # Usar np.nan para valores faltantes
        return valores + [np.nan]  # Añadir np.nan para la columna no_informacion
    except NoSuchElementException:
        print(f"No se encontró la información general para el NIT: {self.nit}")
        return [np.nan] * 15 + [self.nit]  # Retorna una fila con NaN y el NIT en no_informacion

def main():
    EDGE_DRIVER_PATH = r'C:\WebDriver\msedgedriver.exe'
    url = "https://ruesfront.rues.org.co/"

    # obtener los nits desde impala
    query = "select distinct identificacion_benef from proceso_auditoria.radegre limit 10"
    nits_df = extraer_datos(query)
    nits = nits_df['identificacion_benef'].tolist()
    resultados = []
  
    columnas = ['Identificación', 'Categoria de la Matrícula','Tipo de Sociedad','Tipo Organización','Cámara de Comercio',
                'Número de Matrícula','Fecha de Matrícula','Fecha de Vigencia','Estado de la matrícula',
                'Fecha de renovación', 'Último año renovado', 'Fecha de Actualización', 'Emprendimiento Social','Extinción de Dominio', 'Actividad Económica', "No_información"]

    for nit in nits:
        scraper = DatosRues(nit, EDGE_DRIVER_PATH, url)
        valores = scraper.ejecutar()
        if valores:
            resultados.append(valores)
    
    df = pd.DataFrame(resultados, columns=columnas)
    df.to_excel('Resultado_rues.xlsx', index=False)

    # subir el archivo a la lz
    scraper.SubirTabla()

if __name__ == "__main__":
    main()