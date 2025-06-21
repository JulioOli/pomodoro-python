import time
import os
import sys
import select
import threading
import signal
from playsound import playsound

# Variável global para controlar a pausa
paused = False
running = True

def signal_handler(sig, frame):
    """Manipulador de sinal para Ctrl+C."""
    global running
    running = False
    print("\n\nTimer Pomodoro interrompido. Bom trabalho!")
    sys.exit(0)

def check_for_space():
    """Verifica se a barra de espaço foi pressionada usando select."""
    global paused
    try:
        # Verifica se há input disponível no stdin
        if select.select([sys.stdin], [], [], 0.1)[0]:
            key = sys.stdin.read(1)
            if key == ' ':
                paused = not paused
                if paused:
                    print("\n⏸️  PAUSADO - Pressione ESPAÇO novamente para continuar...")
                else:
                    print("\n▶️  CONTINUANDO...")
                return True
            elif key == '\x03':  # Ctrl+C
                signal_handler(None, None)
    except:
        pass
    return False

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

def get_terminal_height():
    """Retorna a altura atual do terminal."""
    try:
        return os.get_terminal_size().lines
    except OSError:
        return 24

def countdown(minutes, title):
    """Função de contagem regressiva com funcionalidade de pausa."""
    global paused, running
    seconds = minutes * 60
    
    while seconds >= 0 and running: #alterei para >= pra mostrar 00:00
        # Verifica se a barra de espaço foi pressionada
        check_for_space()
        
        # Verifica se está pausado
        if paused:
            terminal_width = get_terminal_width()
            timer_display = f"{title}: {seconds//60:02d}:{seconds%60:02d} [PAUSADO]"
            print(timer_display.center(terminal_width), end="\r")
            # Aguarda até que a pausa seja removida
            while paused and running:
                check_for_space()
                time.sleep(0.1)
            if not running:
                break
            # Limpa a linha após despausar para evitar problemas de alinhamento
            print(" " * terminal_width, end="\r")
            continue

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
    global paused, running
    ciclos = 0
    
    # Configura o terminal para modo raw (captura teclas sem Enter)
    old_settings = None
    fd = None
    try:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
    except:
        print("⚠️  Aviso: Funcionalidade de pausa pode não funcionar corretamente neste terminal.")
    
    try:
        while running:
            ciclos += 1
            clear_screen()

            terminal_width = get_terminal_width()
            terminal_height = get_terminal_height()

          # Exibe o título centralizado
            print("\n\n\n\n")
            print(f"⊙ Ciclo de Pomodoro Nº {ciclos} ⊙".center(terminal_width))
            print("\n") #adiciona uma linha em branco pra espaçamento
            
            # Período de Estudo
            countdown(22, "FOCO")
            if not running:
                break
            print("\n")
            print("Dá um tempo aí filho, vai fazer malabarismo ou uns burpies sla..\n\n".center(terminal_width))
            playsound('ok-desu-ka.mp3')

            # Período de Descanso
            countdown(8, "DESCANSO")
            if not running:
                break
            print("\n")
            print("Cabô os 8 min de tédio, bora voltar a Estudar!!\n\n".center(terminal_width))
            playsound('ok-desu-ka.mp3')

    except KeyboardInterrupt:
        print("\n\nTimer Pomodoro interrompido. Bom trabalho!".center(terminal_width))
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
        print("Certifique-se de que o arquivo 'ok-desu-ka.mp3' está na mesma pasta que o script.")
    finally:
        # Restaura as configurações do terminal
        if old_settings and fd:
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass

def show_help():
    """Mostra a dica na parte inferior do terminal."""
    terminal_width = get_terminal_width()
    terminal_height = get_terminal_height()
    
    # Move o cursor para a parte inferior
    print(f"\033[{terminal_height};0H", end="")
    print("Press Ctrl+C para sair".center(terminal_width))

if __name__ == "__main__":
    # Configura o manipulador de sinal para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Mostra a dica na parte inferior
    show_help()
    pomodoro_timer()
