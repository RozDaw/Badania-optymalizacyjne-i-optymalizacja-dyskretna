#include <iostream>

void tsp_rand(int size, unsigned int seed)
{ 
  std::cout<<"data: "<<size<<"\n";  
  for(int a=0; a<size; a++){
    for(int b=0; b<size; b++){
      seed=(seed*69069+1)&0xFFFFFFFF;
      int d=(seed%99+1)*(a!=b);
      std::cout.width(2);
      std::cout<<d<<" ";}
    std::cout<<"\n";}
  std::cout<<std::endl;
}

int main()
{
  for(int i=10;i<21;i++) 
    tsp_rand(i,i);
  return 0;
}
