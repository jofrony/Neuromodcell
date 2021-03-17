#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _bk_reg(void);
extern void _cadyn_reg(void);
extern void _cal12_reg(void);
extern void _cal13_reg(void);
extern void _caldyn_reg(void);
extern void _can_reg(void);
extern void _caq_reg(void);
extern void _car_reg(void);
extern void _cat32_reg(void);
extern void _cat33_reg(void);
extern void _concACh_reg(void);
extern void _concDA_reg(void);
extern void _Im_reg(void);
extern void _kaf_reg(void);
extern void _kas_reg(void);
extern void _kdr_reg(void);
extern void _kir_reg(void);
extern void _naf_reg(void);
extern void _NO_reg(void);
extern void _sk_reg(void);
extern void _tmgabaa_reg(void);
extern void _tmglut_M1RH_D1_reg(void);
extern void _tmglut_reg(void);
extern void _vecevent_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," mechanisms-dspn//bk.mod");
    fprintf(stderr," mechanisms-dspn//cadyn.mod");
    fprintf(stderr," mechanisms-dspn//cal12.mod");
    fprintf(stderr," mechanisms-dspn//cal13.mod");
    fprintf(stderr," mechanisms-dspn//caldyn.mod");
    fprintf(stderr," mechanisms-dspn//can.mod");
    fprintf(stderr," mechanisms-dspn//caq.mod");
    fprintf(stderr," mechanisms-dspn//car.mod");
    fprintf(stderr," mechanisms-dspn//cat32.mod");
    fprintf(stderr," mechanisms-dspn//cat33.mod");
    fprintf(stderr," mechanisms-dspn//concACh.mod");
    fprintf(stderr," mechanisms-dspn//concDA.mod");
    fprintf(stderr," mechanisms-dspn//Im.mod");
    fprintf(stderr," mechanisms-dspn//kaf.mod");
    fprintf(stderr," mechanisms-dspn//kas.mod");
    fprintf(stderr," mechanisms-dspn//kdr.mod");
    fprintf(stderr," mechanisms-dspn//kir.mod");
    fprintf(stderr," mechanisms-dspn//naf.mod");
    fprintf(stderr," mechanisms-dspn//NO.mod");
    fprintf(stderr," mechanisms-dspn//sk.mod");
    fprintf(stderr," mechanisms-dspn//tmgabaa.mod");
    fprintf(stderr," mechanisms-dspn//tmglut_M1RH_D1.mod");
    fprintf(stderr," mechanisms-dspn//tmglut.mod");
    fprintf(stderr," mechanisms-dspn//vecevent.mod");
    fprintf(stderr, "\n");
  }
  _bk_reg();
  _cadyn_reg();
  _cal12_reg();
  _cal13_reg();
  _caldyn_reg();
  _can_reg();
  _caq_reg();
  _car_reg();
  _cat32_reg();
  _cat33_reg();
  _concACh_reg();
  _concDA_reg();
  _Im_reg();
  _kaf_reg();
  _kas_reg();
  _kdr_reg();
  _kir_reg();
  _naf_reg();
  _NO_reg();
  _sk_reg();
  _tmgabaa_reg();
  _tmglut_M1RH_D1_reg();
  _tmglut_reg();
  _vecevent_reg();
}
