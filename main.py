import qiskit
from qiskit import QuantumCircuit
from qiskit.visualization import visualize_transition
import numpy as np
import tkinter
from tkinter import LEFT, END, DISABLED, NORMAL

# Define Window
root = tkinter.Tk()
root.title("Quantalizer")

# Set the icon
root.iconbitmap(default = "logo.ico")
root.geometry("399x410")
root.resizable(0,0) # Blocks the resizing feature

# Define the colors and fonts
background = "#ffffff" 
buttons = "#ffe4c4"
row1_bg = "#fae3c8"
clear_bg = "#f7e5ba"
quit_about_bg = "#f5e2b3"
visualize_bg = "#f7e1ab"
hadamard_bg = "#ffe4c4"
st_bg = "#ffe4c4"
button_font = ("Arial", 18)
display_font = ("Arial", 32)

# Initialize the Quantum Circuit
def initialize_circuit():
  global CIRCUIT
  CIRCUIT = QuantumCircuit(1)

initialize_circuit()
theta = 0

# Define Functions
def display_gate(gate_input):
  """
  Adds a corresponding gate notation in the display to track the operations.
  If number of operations reaches ten, all gate buttons are disabled.
  """

  # Insert the defined gate
  display.insert(END, gate_input)

  # Check if number of operations has reached ten, if yes,
  # disable all the gate buttons
  input_gates = display.get()
  num_gates_pressed = len(input_gates)
  list_input_gates = list(input_gates)
  search_word = ["R", "†"]
  count_double_valued_gates = [list_input_gates.count(i) for i in search_word]
  num_gates_pressed -= sum(count_double_valued_gates)
  if num_gates_pressed == 10:
    gates = [x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
    for gate in gates:
      gate.config(state = DISABLED)

def clear(CIRCUIT):
  """
  Clears the display!
  Reinitializes the Quantum Circuit for fresh calculations!
  Checks if gate buttons are disabled, if so, enables the buttons.
  """

  # Clear the display
  display.delete(0, END)

  # reset the circuit to initial state |0>
  initialize_circuit()

  # check if buttons are disabled, if so, enable them
  if x_gate["state"] == DISABLED:
    gates = [x_gate, y_gate, z_gate, Rx_gate, Ry_gate, Rz_gate, s_gate, sd_gate, t_gate, td_gate, hadamard]
    for gate in gates:
      gate.config(state = NORMAL)

# Define function for about
def about():
  """ 
  Displays information about project
  """
  
  info = tkinter.Tk()
  info.title("About")
  info.geometry("650x470")
  info.resizable(0,0)

  text = tkinter.Text(info, height = 20, width = 20)

  # Create Label
  label = tkinter.Label(info, text = "Quantalizer")
  label.config(font = ("Arial", 14))

  text_to_display = """
  Visualization for Single Qubit Rotation on Bloch Sphere
  Created by: Madhav Parmar

  Information about gate buttons corresponding to their qiskit commands:

  X:  Flips the state of qubit                               circuit.x()
  Y:  Rotates the state vector about Y-axis                  circuit.y()
  Z:  Flips the Z by PI radians                              circuit.z()
  Rx: Parameterized rotation about the X-axis                circuit.rx()
  Ry: Parameterized rotation about the Y-axis                circuit.ry()
  Rz: Parameterized rotation about the Z-axis                circuit.rz()
  S:  Rotates the state vector about Z-axis by π/2 radians   circuit.s()
  T:  Rotates the state vector about Z-axis by π/4 radians   circuit.t()
  SD: Rotates the state vector about Z-axis by -π/2 radians  circuit.sdg()
  TD: Rotates the state vector about Z-axis by -π/4 radians  circuit.tdg()
  H:  Creates the state of superposition                     circuit.h()

  For Rx, Ry and Rz,
  θ ranges between [-2π, 2π]

  In case of visualization error, app closes automatically.
  This indicates the visualization of the circuit provided is not possible.

  Only 10 operations can be visualized at once.
  """

  label.pack()
  text.pack(fill = "both", expand = True)

  # Insert the text
  text.insert(END, text_to_display)

  # Run
  info.mainloop()

def visualize_circuit(CIRCUIT, window):
  """
  Visualizes the single cubit rotations corresponding to applied gates in a seperate tkinter window.
  Handles any possible visualization error
  """

  try:
    visualize_transition(circuit = CIRCUIT)
  except qiskit.visualization.exceptions.VisualizationError:
    window.destroy()

# Change theta
def change_theta(num, window, CIRCUIT, key):
  """
  Changes the global variable theta and destroys window
  """
  global theta
  theta = num * np.pi
  if key == "x":
    CIRCUIT.rx(theta, 0)
    theta = 0
  elif key == "y":
    CIRCUIT.ry(theta, 0)
    theta = 0
  else:
    CIRCUIT.rz(theta, 0)
    theta = 0
  window.destroy()

def user_input(CIRCUIT, key):
  """
  Take the user input for rotation angle for parameterized
  Rotation gates Rx, Ry, Rz.
  """

  # Initialize and define the properties of the window
  get_input = tkinter.Tk()
  get_input.title("θ")
  get_input.geometry("360x88")
  get_input.resizable(0, 0)

  val1 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "π/4", command = lambda: change_theta(0.25, get_input, CIRCUIT, key))
  val1.grid(row = 0, column = 0)

  val2 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "π/2", command = lambda: change_theta(0.5, get_input, CIRCUIT, key))
  val2.grid(row = 0, column = 1)

  val3 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "π", command = lambda: change_theta(1, get_input, CIRCUIT, key))
  val3.grid(row = 0, column = 2)
  
  val4 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "2π", command = lambda: change_theta(2, get_input, CIRCUIT, key))
  val4.grid(row = 0, column = 3, sticky = "W")
  
  nval1 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "-π/4", command = lambda: change_theta(-0.25, get_input, CIRCUIT, key))
  nval1.grid(row = 1, column = 0)
  
  nval2 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "-π/2", command = lambda: change_theta(-0.5, get_input, CIRCUIT, key))
  nval2.grid(row = 1, column = 1)
  
  nval3 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "-π", command = lambda: change_theta(-0.1, get_input, CIRCUIT, key))
  nval3.grid(row = 1, column = 2)
  
  nval4 = tkinter.Button(get_input, height = 2, width = 10, bg = buttons, font = ("Arial", 10), text = "-2π", command = lambda: change_theta(-2, get_input, CIRCUIT, key))
  nval4.grid(row = 1, column = 3, sticky = "W")
  
# Define Frames
display_frame = tkinter.LabelFrame(root)
button_frame = tkinter.LabelFrame(root, bg = "black")
display_frame.pack()
button_frame.pack(fill = "both", expand = True)

# Define the Display Frame Layout
display = tkinter.Entry(display_frame, width = 120, font = display_font, bg = background, borderwidth = 1.5,justify = LEFT)
display.pack(padx = 3, pady = 4)

# Define the first row of Buttons
x_gate = tkinter.Button(button_frame, font = button_font, bg = row1_bg, text = "X", command = lambda: [display_gate("x"), CIRCUIT.x(0)])
y_gate = tkinter.Button(button_frame, font = button_font, bg = row1_bg, text = "Y", command = lambda: [display_gate("y"), CIRCUIT.y(0)])
z_gate = tkinter.Button(button_frame, font = button_font, bg = row1_bg, text = "Z", command = lambda: [display_gate("z"), CIRCUIT.z(0)])
x_gate.grid(row = 0, column = 0, ipadx = 45, pady = 1)
y_gate.grid(row = 0, column = 1, ipadx = 45, pady = 1)
z_gate.grid(row = 0, column = 2, ipadx = 53, pady = 1, sticky = "E")

# Define the second row of Buttons

Rx_gate = tkinter.Button(button_frame, font = button_font, bg = buttons, text = "RX", command = lambda: [display_gate("Rx"), user_input(CIRCUIT, "x")])
Ry_gate = tkinter.Button(button_frame, font = button_font, bg = buttons, text = "RY", command = lambda: [display_gate("Ry"), user_input(CIRCUIT, "y")])
Rz_gate = tkinter.Button(button_frame, font = button_font, bg = buttons, text = "RZ", command = lambda: [display_gate("Rz"), user_input(CIRCUIT, "z")])
Rx_gate.grid(row = 1, column = 0, columnspan = 1, sticky = "WE", pady = 1)
Ry_gate.grid(row = 1, column = 1, columnspan = 1, sticky = "WE", pady = 1)
Rz_gate.grid(row = 1, column = 2, columnspan = 1, sticky = "WE", pady = 1)

# Define the third row of Buttons
s_gate = tkinter.Button(button_frame, font = button_font, bg = st_bg, text = "S", command = lambda: [display_gate("S"), CIRCUIT.s(0)])
sd_gate = tkinter.Button(button_frame, font = button_font, bg = st_bg, text = "S†", command = lambda: [display_gate("S†"), CIRCUIT.sdg(0)])
hadamard = tkinter.Button(button_frame, font = button_font, bg = hadamard_bg, text = "H", command = lambda: [display_gate("h"), CIRCUIT.h(0)])
s_gate.grid(row = 2, column = 0, columnspan = 1, sticky = "WE", pady = 1)
sd_gate.grid(row = 2, column = 1, sticky = "WE", pady = 1)
hadamard.grid(row = 2, column = 2, rowspan = 2, sticky = "WENS", pady = 1)

# Define the fourth row of Buttons
t_gate = tkinter.Button(button_frame, font = button_font, bg = st_bg, text = "T", command = lambda: [display_gate("T"), CIRCUIT.t(0)])
td_gate = tkinter.Button(button_frame, font = button_font, bg = st_bg, text = "T†", command = lambda: [display_gate("T†"), CIRCUIT.tdg(0)])
t_gate.grid(row = 3, column = 0, sticky = "WE", pady = 1)
td_gate.grid(row = 3, column = 1, sticky = "WE", pady = 1)

# Define Quit and Visualize Buttons
quit = tkinter.Button(button_frame, font = button_font, bg = quit_about_bg, text = "Quit", command = root.destroy)
visualize = tkinter.Button(button_frame, font = button_font, bg = visualize_bg, text = "Visualize", command = lambda: visualize_circuit(CIRCUIT, root))
quit.grid(row = 4, column = 0, columnspan = 2, sticky = "WE", ipadx = 5, pady = 1)
visualize.grid(row = 4, column = 2, columnspan = 1, sticky = "WE", ipadx = 8, pady = 1)

# Define Clear Button
clear_button = tkinter.Button(button_frame, font = button_font, bg = clear_bg, text = "Clear", command = lambda: clear(CIRCUIT))
clear_button.grid(row = 5, column = 0, columnspan = 3, sticky = "WE")

# Define About Button
about_button = tkinter.Button(button_frame, font = button_font, bg = quit_about_bg, text = "About", command = about)
about_button.grid(row = 6, column = 0, columnspan = 3, sticky = "WE")

# Run the main loop
root.mainloop()
