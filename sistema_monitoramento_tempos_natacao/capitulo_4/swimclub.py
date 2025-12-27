import statistics
import hfpy_utils

CHARTS = "../charts/"
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
    mins_secs, centis = f"{(average/100):.2f}".split('.')
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    average = f"{minutes}:{seconds:0>2}.{centis}"
    return swimmer, age, distance, stroke, times, average, converts #retorna uma tupla com os dados do nadador

def produce_bar_chart(fn):
    
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age} {distance} {stroke})"
    header = f"""<!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                        </head>
                        <body>
                            <h3>{title}</h3>
    """
    body = ""
    for index, time in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[index], 0, from_max, 0, 350)
        body = body + f"""
                            <svg height="30" width="400">
                                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                            </svg> {time} <br/>
        """
    footer = f"""
                            <p>Average time: {average} </p>
                        </body>
                    </html>
    """
    page = header + body + footer
    save_to = f"{CHARTS}{fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)
        
    return save_to
    