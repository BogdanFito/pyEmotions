#include <Trackcv.h>

void setup()
{
  Serial1.begin(115200);
  artintrackInit(1);
}

void loop()
{
  artintrackUpdate( Neural_script_id_emotion);

}