# Minijuego: Puzzle_game

## 📝 Explicación del juego
Es un rompecabezas electrónico donde una imagen es dividida en partes que actúan como fichas. El objetivo principal del juego es ponerlas en orden para reordenar la imagen original; en ese momento, el jugador gana la partida.

---

## 🚀 Prompts Utilizados e Historial de Ajustes

### 1. Prompt Inicial: Creación de la Base del Juego
> **Prompt:** Actua como un expertor en programacion y desarrollador de video juegos y creame un minijuego de la para armar un rompecabezas, desarrollalo en python, ten en cuenta que el jugador se le presena una imagen segmentada y desordenada tiene que mover las piezas individualmente hasta formar la imagen cuando dos piezas que van juntas se unen estas debe de permanecer juntas, tiene que existir niveles para aumentar la dificulta, que principalmenta va marcada por la cantidad de piezas en la que se divide la imagen. Ocupado al menos 25 imagenes que sean libre de derechos de autor. Has que sea totalmente funcional y que el usuario vaya acumulando puntos.

* **Explicación de lo que se pidió a la IA:** Se pidió básicamente la creación de los parámetros básicos del juego.
* **Por qué se ajustó:** Porque la IA arrojó un juego demasiado básico.

### 2. Segundo Prompt: Selección de Nivel y Restricción de Área
> **Prompt:** ok ya pude correrlo pero el juego, el cual corre bien solo prefiero que el jugador pueda seleccionar el nivel que va a jugar al inicio, ademas que las fichas en las que se ha divido la imagen no se pueda salir de recuado que enmarca el rompecabezas, que muestres alguna senal para que el usuario no lo haga

* **Explicación de lo que se pidió a la IA:** Se pidió la incorporación de un menú de selección de nivel y restricciones físicas para las piezas dentro del tablero.
* **Por qué se ajustó:** Porque la IA arrojó un juego que todavía era demasiado básico, sin controles para seleccionar el nivel y sin restricción en el área de juego.

### 3. Tercer Prompt: Sistema de Rejilla (Grid-Snapping) y Botón de Salida
> **Prompt:** Muchisimo mejor gustaria ademas que el cuadro de fondo que mantiene la imagen del rompecabezas tenga delimitada los cuadros y que las fichas cuando se muevan y se suelten siempre caiga en alguno de los cuadro de su ubicacion, considerando que no van a estar dos fichas en un cuadro y no quedaran fichas sin cuadro asi evitamos que se pierdan fichas a la vista del usuario. Agrega ademas un boton de salida

* **Explicación de lo que se pidió a la IA:** Se pidió la delimitación de las fichas del rompecabezas mediante una cuadrícula fija y un sistema de "ajuste automático" (*snapping*).
* **Por qué se ajustó:** Porque la IA arrojó un juego donde, al mover una ficha, esta quedaba sin control, amontonándose unas encima de otras.

---

## 🛠️ Herramientas y Tecnologías
* **Lenguaje:** Python
* **IA de apoyo:** Gemini
* **Editor de código:** VS Code

---

## 👤 Créditos
* **Creador:** Edgar Alexander Constanza Jovel
