import pandas as pd
from datetime import timedelta


class DFSLoader:
    def __init__(self, prints_file, taps_file, pays_file):
        """
        Clase DFSLoader. Genera los DFs para el proceso general. Los mismos solo contienen
        el universo esperado de datos

        Args:
            prints_file (str): Archivo de prints
            taps_file (str): Archivo de taps
            pays_file (str): Archivo de pays
        """
        # Archivos con los cuales se generan los Dataframes para el proceso general
        self.prints_file = prints_file
        self.taps_file = taps_file
        self.pays_file = pays_file

    def get_prints(self):
        """
        Carga el DataFrame de prints

        Returns:
            pd.DataFrame: DataFrame de prints
        """
        try:
            df_prints = pd.read_json(self.prints_file, lines=True)

            # Convierto a date la columna day
            df_prints['day'] = pd.to_datetime(df_prints['day'])

            # agrega la columna value_prop
            df_prints["value_prop"] = df_prints["event_data"].apply(lambda x: x["value_prop"])

            # Dropea la columna event_data
            df_prints = df_prints.drop("event_data", axis=1)

            # Ordena por fecha
            df_prints.sort_values("day", inplace=True)

            return df_prints
        except FileNotFoundError:
            print("Error en get_prints: No se encontro el archivo Json " + self.prints_file)
            raise FileNotFoundError(f"Error en get_prints: No se encontro el archivo Json '{self.prints_file}'.")
        except ValueError:
            print("Error en get_prints: Json invalido. Archivo: " + self.prints_file)
            raise ValueError(f"Error en get_prints: Json invalido. Archivo: '{self.prints_file}'.")
        except Exception as e:
            print("Error en get_prints: Exception al leer el archivo Json: " + self.prints_file)
            print("Exception: ", str(e))
            raise Exception(f"Error en get_prints: Exception al leer prints.json: '{str(e)}'.")

    def get_prints_last_week(self, df_prints):
        """
        Carga el DataFrame de prints (solo contiene los ultimos 7 dias)

        Returns:
            Vector de pd.DataFrame: Vector de DataFrame de prints (7 particiones 1 por dia)
        """
        # Obtengo la fecha maxima
        max_date = df_prints['day'].max()

        # Calculo la fecha de inicio de la ultima semana
        init_date_prints = max_date - timedelta(days=7)
        # print("Prints de la ultima semana  > " + str(init_date_prints))

        # Filtra los registros de la ultima semana
        df_prints_aux = df_prints[df_prints['day'] > init_date_prints]

        # Particiona por dia los prints
        df_prints_parts = []
        for _, partition in df_prints_aux.groupby(pd.Grouper(key="day")):
            df_prints_parts.append(partition)

        return df_prints_parts

    def get_taps(self):
        """
        Carga el DataFrame de taps

        Returns:
            pd.DataFrame: DataFrame de taps
        """
        try:
            df_taps = pd.read_json(self.taps_file, lines=True)
            # Convierto a date la columna day
            df_taps['day'] = pd.to_datetime(df_taps['day'])

            # Agrega la columna value_prop y clicked
            df_taps["value_prop"] = df_taps["event_data"].apply(lambda x: x["value_prop"])
            df_taps["clicked"] = 'Y'

            # Dropea la columna event_data
            df_taps = df_taps.drop("event_data", axis=1)

            return df_taps
        except FileNotFoundError:
            print("Error en get_taps: No se encontro el archivo Json" + self.taps_file)
            raise FileNotFoundError(f"Error en get_taps: No se encontro el archivo Json '{self.taps_file}'.")
        except ValueError:
            print("Error en get_taps: Json invalido. Archivo: " + self.taps_file)
            raise ValueError(f"Error en get_taps: Json invalido. Archivo: '{self.taps_file}'.")
        except Exception as e:
            print("Error en get_taps: Exception al leer el archivo Json: " + self.taps_file)
            print("Exception: ", str(e))
            raise Exception(f"Error en get_taps: Exception al leer taps.json: '{str(e)}'.")

    def get_pays(self):
        """
        Carga el DataFrame de pays

        Returns:
            pd.DataFrame: DataFrame de pays
        """
        try:
            df_pays = pd.read_csv(self.pays_file, sep=",")

            # Convierto a date la columna pay_date
            df_pays['pay_date'] = pd.to_datetime(df_pays['pay_date'])

            return df_pays
        except FileNotFoundError:
            print("Error en get_pays: No se encontro el archivo Csv " + self.pays_file)
            raise FileNotFoundError(f"Error en get_pays: No se encontro el archivo Csv '{self.pays_file}'.")
        except ValueError:
            print("Error en get_pays: Csv invalido. Archivo: " + self.pays_file)
            raise ValueError(f"Error en get_pays: Csv invalido. Archivo: '{self.pays_file}'.")
        except Exception as e:
            print("Error en get_pays: Exception al leer el archivo Csv: " + self.pays_file)
            print("Exception: ", str(e))
            raise Exception(f"Error en get_pays: Exception al leer pays.csv '{str(e)}'.")
