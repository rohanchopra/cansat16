int i;
int temp;
char reading[128];
void setup() { 
  
  Serial.begin(9600); 
  i=1;

} 


void loop() { 
  //sprintf(reading,"132,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d"
  //      ,i,random(1,1000),random(1,1000),random(1,100),random(1,30),random(1,10),random(1,100),random(1,100),random(1,1000),random(1,6),random(1,100),random(1,100),i);
  //Serial.println(reading);
  Serial.print("132,");
  Serial.print(i);    
  Serial.print(",");  
  temp =   random(1,1000);
  Serial.print(temp);  
  Serial.print(",");    
  Serial.print(temp);    
  Serial.print(",");  
  temp =   random(1,100);
  Serial.print(temp);    
  Serial.print(",");  
  temp =   random(1,30);
  Serial.print(temp);      
  Serial.print(",");  
  temp =   random(1,10);
  Serial.print(temp);    
  Serial.print(",");  
  temp =   random(1,100);
  Serial.print(temp);  
  Serial.print(",");    
  temp =   random(1,100);
  Serial.print(temp);      
  Serial.print(",");
  temp =   random(1,1000);
  Serial.print(temp);    
  Serial.print(","); 
  temp =   random(1,6);
  Serial.print(temp);      
  Serial.print(",");
  temp =   random(1,100);
  Serial.print(temp);        
  Serial.print(",");
  temp =   random(1,100);
  Serial.print(temp);     
  Serial.print(",");
  Serial.println(i);

  delay(1000);
  
  i++;
} 
