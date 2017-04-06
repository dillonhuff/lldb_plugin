#include <iostream>

#include "contrived.h"

using namespace std;

int main() {
  int x = 2;
  int y = 4;
  int z = 9;

  bool useless = true;

  my_value v{x, y, z, useless};
  int k = contrived_1(3, 4, -12, v);

  cout << k << endl;
}
