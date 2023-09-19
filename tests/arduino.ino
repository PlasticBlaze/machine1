// I have an arduino board with a motor shield on top to drive the wheels. I have written a couple commands in here but still need to add like all of the refinement,
// tool offset, out-of-boundary, and routine commands that pertain to the driving of the bot.



#include <AccelStepper.h>

const int stepperCount = 4;
AccelStepper BLStepper(1, 2, 5);
AccelStepper FLStepper(1, 3, 6);
AccelStepper FRStepper(1, 4, 7);
AccelStepper BRStepper(1, 12, 13);

bool movementComplete = false;

// defines pins numbers

//Front left wheel
const int stepX = 2;
const int dirX  = 5;

//Front right wheel
const int stepY = 3;
const int dirY  = 6;

//Back left wheel
const int stepZ = 4;
const int dirZ  = 7;

//Back right wheel
const int stepA = 12;
const int dirA  = 13;
const int enPin = 8;


char split = ':';         //this is the character that would be used for seperating the different parts of your commands
                          //the syntax for commands would be:   command:value1:value2

int listSize = 5;                                     //the amount of commands in the list
String commands[] = {"hello", "add", "toolOFFSET", "YMOV", "XMOV"};     //the list of every command name


void setup() 
{
  Serial.begin(115200);     
                          
                          
  FRStepper.setMaxSpeed(300);
  FRStepper.setAcceleration(200);
  BRStepper.setMaxSpeed(300);
  BRStepper.setAcceleration(200);
  
  FLStepper.setMaxSpeed(300);
  FLStepper.setAcceleration(200);
  BLStepper.setMaxSpeed(300);
  BLStepper.setAcceleration(200);

  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  
  pinMode(stepY, OUTPUT);
  pinMode(dirY, OUTPUT);
  
  pinMode(stepZ, OUTPUT);
  pinMode(dirZ, OUTPUT);

  pinMode(enPin, OUTPUT);

  digitalWrite(enPin, LOW);
  digitalWrite(dirX, HIGH);
  digitalWrite(dirY, HIGH);
  digitalWrite(dirZ, HIGH);
  digitalWrite(dirA, HIGH);


}

void loop() 
{
  CommCheck(); //checks serial buffer for data commands
  runMotors();
 
}

void runMotors()
{

  if ((FLStepper.distanceToGo() != 0) || (FRStepper.distanceToGo() != 0) || (BLStepper.distanceToGo() != 0) || (BRStepper.distanceToGo() != 0))
  {
    
    //FLStepper.run();
    //BLStepper.run();
    //FRStepper.run();
    //BRStepper.run();
    
    if ((FLStepper.distanceToGo() == 0) && (FRStepper.distanceToGo() == 0))
    {
      CommConfirm();
    }
  }
  
  //if (movementComplete == true)
  //{
    //CommConfirm();
  //}
  //if (
  //if ((FLStepper.distanceToGo() == 0) || (FRStepper.distanceToGo() == 0) || (BLStepper.distanceToGo() == 0) || (BRStepper.distanceToGo() == 0))
  //{
    //CommConfirm();
  //}
}
void CommCheck()
{
  if(Serial.available())                    //checks to see if there is serial data has been received
  {
    //int len = Serial.available();           //stores the character lengh of the command that was sent
                                             //this is used for command parsing later on
                                            
    String command = Serial.readString();   //stores the command as a text string
    int len = command.length();
    //Serial.println(command);
    Serial.flush();
    //command.remove(len-2,1);                //removes characters added by the pi's serial data protocol
    //command.remove(0,2);
    //len -= 3;                               //updates the string length value for parsing routine

    int points[2] = {0, 0};                 //offset points for where we need to split the command into its individual parts
    
    for(int x = 0; x < len; x++)            //this loop will go through the entire command to find the split points based on
    {                                       //what the split variable declared at the top of the script is set to.
      //Serial.print("Char ");
      //Serial.print(x);
      //Serial.print("- ");
      //Serial.println(command[x]);
      if(command[x] == split)               //this goes through every character in the string and compares it to the split character
      {
        if(points[0] == 0)                  //if the first split point hasn't been found, set it to the current spot
        {
          points[0] = x;
        }
        else                                //if the first spot was already found, then set the second split point
        {                                   //this routine is currently only set up for a command syntax that is as follows
          points[1] = x;                    //command:datavalue1:datavalue2
        }
      }
    }
    CommParse(command, len, points[0], points[1]);      //now that we know the command, command length, and split points,
  }                                                     //we can then send that information out to a routine to split the data
}                                                       //into individual values.

void CommParse(String command, int len, int point1, int point2)
{
  //Serial.print("Command Length: ");
  //Serial.println(len);
  //Serial.print("Split 1: ");
  //Serial.println(point1);
  //Serial.print("Split 2: ");
  //Serial.println(point2);

  
  String com = command;                 //copy the full command into all 3 parts
  String val1 = command;                //this is needed for the string manipulation
  String val2 = command;                //that follow

  com.remove(point1, len - point1);     //each of these use the string remove to delete
  val1.remove(point2, len - point2);    //the parts of the command that aren't needed
  val1.remove(0, point1 + 1);           //basically splitting the command up into its
  val2.remove(0, point2 + 1);           //individual pieces
  val2.remove(val2.length()-1,1);

  CommLookup(com, val1, val2);    //these pieces are then sent to a lookup routine for processing
}


void CommLookup(String com, String val1, String val2)
{
  
  int offset = 255;                   //create a variable for our lookup table's offest value
                                      //we set this to 255 because there won't be 255 total commands
                                      //and a valid command can be offset 0, so it's just to avoid
                                      //any possible coding conflicts if the command sent doesn't
                                      //match anything.
                                      
  for(int x = 0; x < listSize; x++)   //this goes through the list of commands and compares 
  {                                   //them against the command received
    if(commands[x] == com)
    {
      offset = x;                     //if the command matches one in the table, store that command's offset
    }
  }
  
  switch(offset)                //this code compares the offset value and triggers the appropriate command
  {
    case 0:                                 //essentially a hello world.                       |  Syntax: hello:null:null
      CommHello();                          //this activates the hello world subroutine        |  returns Hello!
      break;
    case 1:                                 //adds both values together and return the sum.    |  Syntax: add:value1:value2
      CommAdd(val1.toInt(), val2.toInt());  //this activates the addition subroutine           |  returns value1 + value2
      break;
    case 2:                                 //subtracts both values and return the difference  |  Syntax: subtract:value1:value2
      CommSub(val1.toInt(), val2.toInt());  //this activates the subtraction subroutine        |  returns value1 - value2
      break;
    case 3:
      yMovement(val1.toInt(), val2.toInt());
      break;
    case 4:
      xMovement(val1.toInt(), val2.toInt());
    default:                                        //this is the default case for the command lookup and will only
      Serial.println("Command not recognized");     //trigger if the command sent was not known by the arduino
      break;
  }
}


void CommHello()                               //each of these routines are what will be triggered when they are successfully processed
{
  Serial.println("Hello!");
  CommConfirm();
}

void CommAdd(int val1, int val2)
{
  Serial.println(val1 + val2);
  CommConfirm();
}

void toolOFFSET(int val1, int val2)
{
for(int x = 0; x < (1000); x++) {              //CHANGE THIS VALUE FOR TOOL OFFSET

      digitalWrite(dirX, HIGH);
      digitalWrite(stepX,HIGH);
      digitalWrite(dirY, HIGH);
      digitalWrite(stepY,HIGH);
      digitalWrite(dirZ, HIGH);
      digitalWrite(stepZ,HIGH);
      digitalWrite(dirA, HIGH);
      digitalWrite(stepA,HIGH);

      delayMicroseconds(250);

      digitalWrite(stepX,LOW);
      digitalWrite(stepY,LOW);
      digitalWrite(stepZ,LOW);
      digitalWrite(stepA,LOW);

      delayMicroseconds(250);
    }
    CommConfirm();
}

void yMovement(int val1, int val2)
{
  if (val1 < 0) {
    //Serial.println("YMOVNEG");
    int yMoveNew = (val1 * (-41.44));
    
    //FRStepper.move(-yMoveNew);
    //BRStepper.move(-yMoveNew);
    //FLStepper.move(-yMoveNew);
    //BLStepper.move(-yMoveNew);

    for(int x = 0; x < (yMoveNew); x++) {

      digitalWrite(dirX, LOW);
      digitalWrite(stepX,HIGH);
      digitalWrite(dirY, LOW);
      digitalWrite(stepY,HIGH);
      digitalWrite(dirZ, LOW);
      digitalWrite(stepZ,HIGH);
      digitalWrite(dirA, LOW);
      digitalWrite(stepA,HIGH);

      delayMicroseconds(250);

      digitalWrite(stepX,LOW);
      digitalWrite(stepY,LOW);
      digitalWrite(stepZ,LOW);
      digitalWrite(stepA,LOW);

      delayMicroseconds(250);
    }
    CommConfirm();
  }

  else {
    //Serial.println(val1);
    int yMoveNew = (val1 * (41.44));

    //FRStepper.move(yMoveNew);
    //BRStepper.move(yMoveNew);
    //FLStepper.move(yMoveNew);
    //BLStepper.move(yMoveNew);

    for(int x = 0; x < (yMoveNew); x++) {

      digitalWrite(dirX, HIGH);
      digitalWrite(stepX,HIGH);
      digitalWrite(dirY, HIGH);
      digitalWrite(stepY,HIGH);
      digitalWrite(dirZ, HIGH);
      digitalWrite(stepZ,HIGH);
      digitalWrite(dirA, HIGH);
      digitalWrite(stepA,HIGH);

      delayMicroseconds(250);

      digitalWrite(stepX,LOW);
      digitalWrite(stepY,LOW);
      digitalWrite(stepZ,LOW);
      digitalWrite(stepA,LOW);

      delayMicroseconds(250);
    }
    CommConfirm();
  }

}

void xMovement(int val1, int val2)
{
  if (val1 < 0) {
    //Serial.println(val1);
    int xMoveNew = (val1 * (-41.44));

    //FLStepper.move(-xMoveNew);
    //BLStepper.move(xMoveNew);
    //FRStepper.move(xMoveNew);
    //BRStepper.move(-xMoveNew);
    
    for(int x = 0; x < (xMoveNew); x++) {

      digitalWrite(dirX, HIGH);
      digitalWrite(stepX,HIGH);
      digitalWrite(dirY, LOW);
      digitalWrite(stepY,HIGH);
      digitalWrite(dirZ, HIGH);
      digitalWrite(stepZ,HIGH);
      digitalWrite(dirA, LOW);
      digitalWrite(stepA,HIGH);

      delayMicroseconds(250);

      digitalWrite(stepX,LOW);
      digitalWrite(stepY,LOW);
      digitalWrite(stepZ,LOW);
      digitalWrite(stepA,LOW);

      delayMicroseconds(250);
    }
    CommConfirm();

    //delayMicroseconds(500);
    
  }

  else {

    int xMoveNew = (val1 * (41.44));

    //FLStepper.move(xMoveNew);
    //BLStepper.move(xMoveNew);
    //FRStepper.move(xMoveNew);
    //BRStepper.move(xMoveNew);

    for(int x = 0; x < (xMoveNew); x++) {

      digitalWrite(dirX, LOW);
      digitalWrite(stepX,HIGH);
      digitalWrite(dirY, HIGH);
      digitalWrite(stepY,HIGH);
      digitalWrite(dirZ, LOW);
      digitalWrite(stepZ,HIGH);
      digitalWrite(dirA, HIGH);
      digitalWrite(stepA,HIGH);

      delayMicroseconds(250);

      digitalWrite(stepX,LOW);
      digitalWrite(stepY,LOW);
      digitalWrite(stepZ,LOW);
      digitalWrite(stepA,LOW);

      delayMicroseconds(250);
    }
    CommConfirm();

    //delayMicroseconds(500);
    
  }
}
void CommConfirm()                                   
{                                                     
  Serial.println("Done");
  delay(750);
  
}
