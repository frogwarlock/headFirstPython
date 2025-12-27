import statistics

FOLDER = '../swimdata/'

def read_swim_data(filename):
    """Retorna os dados de natação de um arquivo.

    Args:
        filename (string): recebe uma string com o nome do arquivo a ser lido

    Returns:
        tuple: retorna uma tupla com as informações do nadador, idade, distância, estilo, lista de tempos e tempo médio
    """
    swimmer, age, distance, stroke = filename.removesuffix('.txt').split('-')
    with open(FOLDER + filename) as file:
        lines =file.readlines()
        times = lines[0].strip().split(',')
    converts = []
    for time in times:
        # o valor de minutes pode não existir, então é necessário verificar
        if ":" in time:
            minutes, rest = time.split(':')
            seconds, centis = rest.split('.')
        else:
            minutes = '0'
            seconds, centis = time.split('.')
        converts.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(centis))
    average = statistics.mean(converts)
    mins_secs, centis = str(round(average/100,2)).split('.')
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    average = str(minutes) + ':' + str(seconds) + '.' + str(centis)
    return swimmer, age, distance, stroke, times, average #retorna uma tupla com os dados do nadador