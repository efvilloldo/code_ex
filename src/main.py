from do_result import do_result
from DFSLoader import DFSLoader


def main():
    # Archivos a leer
    prints_file = './local/prints.json'
    taps_file = './local/taps.json'
    pays_file = './local/pays.csv'

    # Crear una instancia de la clase DFSLoader
    loader = DFSLoader(prints_file, taps_file, pays_file)

    # Cargar los DataFrames utilizando los métodos correspondientes
    df_prints = loader.get_prints()

    # Prints de la ultima semana
    df_prints_last_week = loader.get_prints_last_week(df_prints)

    # dfs de taps y pays
    df_taps = loader.get_taps()
    df_pays = loader.get_pays()

    # Arma el resultado
    df_result = do_result(df_prints_last_week, df_prints, df_taps, df_pays)
    # Graba el dataframe generado en un CSV
    df_result.to_csv('Result.csv', index=False, sep=',')
    print("Archivo generado 'Result.csv'. Registros generados: " + str(len(df_result)))


if __name__ == '__main__':
    main()
