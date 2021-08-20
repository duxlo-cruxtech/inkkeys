//Display
const byte PIN_DIN = 16;
const byte PIN_CLK = 15;
const byte PIN_CS = 13;
const byte PIN_DC = 5;
const byte PIN_RST = 10;
const byte PIN_BUSY = 14;

//Display size
const short DISP_W = 128; //Dispaly width
const short DISP_H = 296; //Display height

//LEDs
const byte PIN_LED = 6;
const byte N_LED = 20; //Number of LEDs

//Rotary encoder
const byte PIN_ROTA = 0;
const byte PIN_ROTB = 1;
const byte PIN_SW1 = 9; // Map this switch to LEDs 8 through 19

const byte ROT_FACTOR = 4;         //Smallest reported step, typically one "click" on the encoder 
const byte ROT_CIRCLE_STEPS = 64;  //Rotary steps in a full circle

//Keys
const byte PIN_SW2 = 3; // Map to LED4
const byte PIN_SW3 = 2; // Map to LED5
const byte PIN_SW4 = 4; // Map to LED6
const byte PIN_SW5 = 12;// Map to LED7
const byte PIN_SW6 = A4;// Map to LED0
const byte PIN_SW7 = A3;// Map to LED1
const byte PIN_SW8 = A2;// Map to LED2
const byte PIN_SW9 = A1;// Map to LED3

const int DEBOUNCE_TIME = 50; //Debounce reject interval in milliseconds
