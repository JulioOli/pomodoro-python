import time
import os
from playsound import playsound

def clear_screen():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    """Retorna a largura atual do terminal."""
    try:
        # Tenta obter o tamanho do terminal. Funciona na maioria dos sistemas.
        return os.get_terminal_size().columns
    except OSError:
        # Se não conseguir (ex: rodando em um ambiente não-padrão), retorna um valor padrão.
        return 80

def countdown(minutes, title):
    """Função de contagem regressiva."""
    seconds = minutes * 60
    while seconds >= 0: #alterei para >= pra mostrar 00:00

        # Prepara o título centralizado
        terminal_width = get_terminal_width()

        mins, secs = divmod(seconds, 60)
        timer = f'{title}: {mins:02d}:{secs:02d}'
        
        print(timer.center(terminal_width), end="\r")
        time.sleep(1)
        seconds -= 1
    print() # Pula para a próxima linha ao final da contagem

def pomodoro_timer():
    """Inicia os ciclos de estudo e descanso do Pomodoro."""
    ciclos = 0
    try:
        while True:
            ciclos += 1
            clear_screen()

            terminal_width = get_terminal_width()

          # Exibe o título centralizado
            print("\n\n\n\n")
            print(f"⊙ Ciclo de Pomodoro Nº {ciclos} ⊙".center(terminal_width))
            print("\n") #adiciona uma linha em branco pra espaçamento
            
            # Período de Estudo
            countdown(22, "FOCO")
            print("\n")
            print("Dá um tempo aí filho, vai fazer malabarismo ou uns burpies sla..")
            playsound('ok-desu-ka.mp3')

            # Período de Descanso
            countdown(8, "DESCANSO")
            print("\n")
            print("Cabô os 8 min de tédio, bora voltar a Estudar!!")
            playsound('ok-desu-ka.mp3')

    except KeyboardInterrupt:
        print("\nTimer Pomodoro interrompido. Bom trabalho!")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Certifique-se de que o arquivo 'ok-desu-ka.mp3' está na mesma pasta que o script.")

if __name__ == "__main__":
    pomodoro_timer()
