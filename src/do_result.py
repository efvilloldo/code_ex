import pandas as pd
from datetime import timedelta


def do_result(df_prints_last_week, df_prints, df_taps, df_pays):
    """
    Determina un DF con los prints de los ultimos 7 dias, calculando los views, pays
    y pays por usuario y value_prop.

    Args:
        df_prints_last_week (DataFrame): df de prints de la ultima semana
        df_prints (DataFrame): df de prints
        df_taps (DataFrame): df de clicks
        df_pays (DataFrame): df de pagos

    Returns:
        pd.DataFrame: DataFrame resultante del join.
    """
    # Define el dataframe de salida vacio
    df_result = pd.DataFrame()

    # Recorre los prints de la ultima semana y calcula el resultado
    for df_print_item in df_prints_last_week:
        # dia a procesar
        day = df_print_item['day'].unique()[0]

        # 3 semanas para atras desde el dia a procesar
        init_day = day - timedelta(weeks=3)
        print('Procesando dia ' + str(day) + ' con historia hasta ' + str(init_day))

        # prints correspondientes al dia a procesar
        df_prints_group = df_prints[
            (df_prints['day'] >= init_day) & (df_prints['day'] < day)
        ].groupby(["value_prop", "user_id"]).size().reset_index(name="print_count")

        # taps correspondientes al dia a procesar
        df_taps_group = df_taps[
            (df_taps['day'] >= init_day) & (df_taps['day'] < day)
        ].groupby(["value_prop", "user_id"]).size().reset_index(name="tap_count")

        # pays correspondientes al dia a procesar
        df_pays_group = df_pays[(df_pays['pay_date'] >= init_day) & (df_pays['pay_date'] < day)]
        df_pays_group = df_pays_group.groupby(["user_id", "value_prop"]) \
                                     .agg({"pay_date": "count", "total": "sum"}).reset_index()
        df_pays_group.rename(columns={"pay_date": "pay_count", "total": "pay_amount"}, inplace=True)

        # Arma el resultado
        # Realiza un join entre df_prints_gruop, df_taps_group y df_pays_group

        # Join para obtener el clicked
        df_join = df_print_item.merge(df_taps, on=["day", "user_id", "value_prop"],
                                      how="left").fillna('N')
        # Join para obtener el print_count
        df_join = df_join.merge(df_prints_group, on=["user_id", "value_prop"], how="left")
        # Join para obtneer el tap_count
        df_join = df_join.merge(df_taps_group, on=["user_id", "value_prop"], how="left")
        # Join para obtener el pay_count y pay_amount y reemplaza los NaN por Ceros
        df_join = df_join.merge(df_pays_group, on=["user_id", "value_prop"], how="left").fillna(0)

        # Concatena el df del dia procesado
        df_result = pd.concat([df_result, df_join])

    return df_result
