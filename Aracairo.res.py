pip install pyTelegramBotAPI
import telebot
import math
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#...............................................................................................................................................
API = '5604449866:AAHjQvm4pSpgNg4o_Fxzhv5XYZVCjvMRxsg'
bot = telebot.TeleBot(token=API)
Dict_epsilon = {"glass":"0",
"plastic":"0",
"wood":"0.0005","rubber":"0.00001",
"castiron":"0.26",
"brass":"0.0000015",
"iron":"0.00015","steel":"0.000002"}
#...............................................................................................................................................
@bot.message_handler(commands=['Head_loss'])
def model1(message):
    inputs = message.text.split()
    Zebri_nesbi = inputs[1].lower() # havaset bashe
    D_pipe = float(inputs[2])  # mm
    L_pipe = float(inputs[3])
    Q_pipe = float(inputs[4])
    Zebri_last = float(Dict_epsilon[Zebri_nesbi]) # havaset be float bashe
    V_cinematic = float(inputs[5])
    if 10**(-6) < (Zebri_last)/(D_pipe) < 10**(-2):
        def Head_loss(Zebri_last,Q_pipe,L_pipe,D_pipe,V_cinematic):
          hf = (1.07*(((Q_pipe**2)*L_pipe)/((D_pipe**5)*9.8)))*((math.log(Zebri_last/(3.7*D_pipe)) + 4.62*((V_cinematic*D_pipe/Q_pipe)**(0.9)))**(-2))
          return hf 
        output = " The head loss is : " + str(Head_loss(Zebri_last,Q_pipe,L_pipe,D_pipe,V_cinematic)) + "  m"
        bot.send_message(message.chat.id, output)
    else:
        bot.send_message(message.chat.id, "Not supported by Swamie Jain equation! ")
#.............................................................................................................................................
@bot.message_handler(commands=['Q_pipe'])
def model2(message):
  inputs = message.text.split()
  Zebri_nesbi = inputs[1].lower()
  D_pipe = float(inputs[2])  # mm
  L_pipe = float(inputs[3])
  h_f = float(inputs[4])
  Zebri_last = float(Dict_epsilon[Zebri_nesbi]) # havaset be float bashe
  V_cinematic = float(inputs[5])
  def Q_pipe(Zebri_last,h_f,L_pipe,D_pipe,V_cinematic):
     A = (-0.965)*((((9.8*h_f)*(D_pipe**5))/L_pipe)**(0.5))
     B = Zebri_last/(3.7*D_pipe)
     C = ((3.17*L_pipe*(V_cinematic**2))/(9.8*h_f*(D_pipe**3)))**0.5
     Q = A*(math.log(B+C))
     return Q
  output = " The flow rate is : " + str(Q_pipe(Zebri_last,h_f,L_pipe,D_pipe,V_cinematic)) + "  m^3/s"
  bot.send_message(message.chat.id, output)
#...........................................................................................................................................
@bot.message_handler(commands=['D_pipe'])
def model3(message):
  inputs = message.text.split()
  Zebri_nesbi = inputs[1].lower()
  Q_pipe = float(inputs[2])  # mm
  L_pipe = float(inputs[3])
  h_f = float(inputs[4])
  Zebri_last = float(Dict_epsilon[Zebri_nesbi]) # havaset be float bashe
  V_cinematic = float(inputs[5])
  def D_pipe(Zebri_last,h_f,L_pipe,Q_pipe,V_cinematic):
        X = (Zebri_last**1.25)
        Y =((L_pipe*(Q_pipe**2))/(9.8*h_f))**4.75
        Z = (V_cinematic)*(Q_pipe**9.4)
        W = ((L_pipe)/(9.8*h_f))**5.2
        D_total = 0.66*(((X*Y) + (Z*W))**0.04)
        return D_total
  output = " The diameter is : " + str(D_pipe(Zebri_last,h_f,L_pipe,Q_pipe,V_cinematic)) + "  m^2"
  bot.send_message(message.chat.id, output)
#...........................................................................................................................................
@bot.message_handler(commands=['start'])
def send_message(message):
  bot.reply_to(message, "welcome to Aracairo bot! Aracairo calculates the head loss, flow rate and diameter of pipes depends on their materials. If you are ready click /ready to go through it!" )
@bot.message_handler(commands=['ready'])
def send_message(message):
  bot.reply_to(message, "Ok let's go! But before, please click /help to know how to use the bot and /more_details for more information about these parameters. And also you can see all commands by /commands")
@bot.message_handler(commands=['help'])
def send_message(message):
  bot.reply_to(message, "Well, First You ought to enter the parameter that you want to calculate. press /Head_loss_pipe for calculating the head loss of a pipe. press /Q_flow to get the flow rate. and click /Diameter to calculate the diameter of the pipe!")
#.............................................................................................................................................
@bot.message_handler(commands=['Head_loss_pipe'])
def send_message(message):
  bot.reply_to(message, "Now enter these parameters:\n1. Material of pipe\n2. Diameter of pipe\n3. Length of pipe\n4. Flow rate\n5. cinematic viscosity\nBe carefull about the format! Enter like this in SI units:\n/Head_loss material D_pipe L_pipe Q_pipe V_cinematic ")
#.............................................................................................................................................
@bot.message_handler(commands=['Q_flow'])
def send_message(message):
  bot.reply_to(message, "Now enter these parameters:\n1. Material of pipe\n2. Diameter of pipe\n3. Length of pipe\n4. Head loss\n5. cinematic viscosity\nBe carefull about the format! Enter like this in SI units:\n/Q_pipe material D_pipe L_pipe h_f V_cinematic")
#.............................................................................................................................................
@bot.message_handler(commands=['Diameter'])
def send_message(message):
  bot.reply_to(message, "Now enter these parameters:\n1. Material of pipe\n2. Flow rate \n3. Length of pipe\n4. Head loss\n5. cinematic viscosity\nBe carefull about the format! Enter like this in SI units:\n/D_pipe material Q_pipe L_pipe h_f V_cinematic")
#.............................................................................................................................................
@bot.message_handler(commands=['time'])
def send_message(message):
  now = datetime.now()
  date_time = now.strftime("%y/%m/%d, %H:%M:%S")
  bot.reply_to(message, date_time)
#..............................................................................................................................................
@bot.message_handler(commands=['more_details'])
def send_message(message):
  bot.reply_to(message,"When you want to calculate the head loss,flow rate and diameter of a pipe in turbulant stream, its important to use empirical equations like Swamee Jain. Using the material, cinematic viscosity and length of pipe, Aracairo will be able to calculate the unknown parameters. There is a list of materials that are used in piping (wood,iron,castiron,steel,brass,plastic,rubber and glass). By the way! Enter a real diameter in order not to get errors! ")
#..............................................................................................................................................
@bot.message_handler(commands=['commands'])
def send_message(message):
  bot.reply_to(message, "/start\n /ready\n /help\n /time\n /more_details\n /Head_loss_pipe\n /Q_flow\n /Diameter\n /commands")

bot.polling()