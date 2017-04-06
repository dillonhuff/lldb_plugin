#include "contrived.h"

int contrived_1(const int l, const int v, const int q, my_value my_v) {
  int r1 = l - v;
  int r2 = q*l;

  if (my_v.useless) {
    return r1 - r2;
  } else {
    return my_v.x + my_v.y + my_v.z - r1*r2;
  }
}
