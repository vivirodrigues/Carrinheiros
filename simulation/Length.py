import Graphs
import scipy.stats
import matplotlib.pyplot as plt
from xml.dom import minidom
import numpy as np


TRABALHO = 'Trabalho'
IMPEDANCIA = "Impedância"
DISTANCIA = "Distância"

PENALIDADE = 'Caminhos mais seguros'
SEM_PENALIDADE = 'Caminhos menos seguros'


def mean_confidence_interval(data, confidence=0.90):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    #return m, m - h, m + h
    return m, h


def plot_dist():

    files = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_speed_False.xml',
        '../data/results/m43.96258893392489_m19.93890742628848_m43.92910823112161_m19.902297290021462_1_weight_speed_False.xml',
        '../data/results/m43.96219206555545_m19.937592627268693_m43.92721201721954_m19.897338285624617_2_weight_speed_False.xml',
        '../data/results/m43.96515130388291_m19.933967721028743_m43.924803225217914_m19.901993293336044_3_weight_speed_False.xml',
        '../data/results/m43.958155756813724_m19.935767178008454_m43.925485937561184_m19.904408612118715_4_weight_speed_False.xml',
        '../data/results/m43.95818027059323_m19.938604532284597_m43.929235631948124_m19.90457942651027_5_weight_speed_False.xml',
        '../data/results/m43.9653853242824_m19.9383851554445_m43.9252111325823_m19.899419689773328_6_weight_speed_False.xml',
        '../data/results/m43.95697862558871_m19.940452374824503_m43.928999369322256_m19.904689345177896_7_weight_speed_False.xml',
        '../data/results/m43.96044454229133_m19.935602569380528_m43.927486971404164_m19.902595967206803_8_weight_speed_False.xml',
        '../data/results/m43.96307765908471_m19.936534694192257_m43.92878346604246_m19.90323786211238_9_weight_speed_False.xml',
        '../data/results/m43.96378669575266_m19.937415550794487_m43.92556976074784_m19.90227285770205_10_weight_speed_False.xml',
        '../data/results/m43.95842463867983_m19.93497835631086_m43.92129512514365_m19.90235042426268_11_weight_speed_False.xml',
        '../data/results/m43.95808331863048_m19.936661310419854_m43.930358792315225_m19.89912528213961_12_weight_speed_False.xml',
        '../data/results/m43.96446085632583_m19.937971076519364_m43.924723463485655_m19.902920711587992_13_weight_speed_False.xml',
        '../data/results/m43.9612355417369_m19.941267713352413_m43.92984863384034_m19.898764680942477_14_weight_speed_False.xml',
        '../data/results/m43.96495075153908_m19.942608827962108_m43.92911774818183_m19.899208956895738_15_weight_speed_False.xml',
        '../data/results/m43.95784918158142_m19.93831108715641_m43.92615622459621_m19.89846196166522_16_weight_speed_False.xml',
        '../data/results/m43.95937989265711_m19.936833980637793_m43.93219982725721_m19.89825689372424_17_weight_speed_False.xml',
        '../data/results/m43.96293961431717_m19.935172607291324_m43.930357106881246_m19.903974461487174_18_weight_speed_False.xml',
        '../data/results/m43.96034011898778_m19.93680839068091_m43.92662329614089_m19.901653732408676_19_weight_speed_False.xml',
        '../data/results/m43.955235672746575_m19.93735112304128_m43.925528706428295_m19.904505533709262_20_weight_speed_False.xml',
        '../data/results/m43.962508248386314_m19.939721380952662_m43.92870408013037_m19.905040976513124_21_weight_speed_False.xml',
        '../data/results/m43.96118206717425_m19.937124071850626_m43.92794882222694_m19.90387030400352_22_weight_speed_False.xml',
        '../data/results/m43.964235089598546_m19.935214304339706_m43.92487114842837_m19.902058670632513_23_weight_speed_False.xml',
        '../data/results/m43.96388328437391_m19.941652310401462_m43.92827617311408_m19.903672220778653_24_weight_speed_False.xml',
        '../data/results/m43.96242426308025_m19.93700754355518_m43.92727190816325_m19.904857644928587_25_weight_speed_False.xml',
        '../data/results/m43.95965160072889_m19.940438581724024_m43.92715932553138_m19.9002848685454_26_weight_speed_False.xml',
        '../data/results/m43.96790910414567_m19.935377000340775_m43.925772351210775_m19.90167005715351_27_weight_speed_False.xml',
        '../data/results/m43.96312957554299_m19.941603786474108_m43.927559952832084_m19.904328777135394_28_weight_speed_False.xml',
        '../data/results/m43.96118516288448_m19.940431956290915_m43.92455170562453_m19.902993970461896_29_weight_speed_False.xml',
        '../data/results/m43.95994424010934_m19.935889252263795_m43.92718563643079_m19.902317407840307_30_weight_speed_False.xml'

    ]

    files_i = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_speed_False.xml',
        '../data/results/m43.96258893392489_m19.93890742628848_m43.92910823112161_m19.902297290021462_1_impedance_speed_False.xml',
        '../data/results/m43.96219206555545_m19.937592627268693_m43.92721201721954_m19.897338285624617_2_impedance_speed_False.xml',
        '../data/results/m43.96515130388291_m19.933967721028743_m43.924803225217914_m19.901993293336044_3_impedance_speed_False.xml',
        '../data/results/m43.958155756813724_m19.935767178008454_m43.925485937561184_m19.904408612118715_4_impedance_speed_False.xml',
        '../data/results/m43.95818027059323_m19.938604532284597_m43.929235631948124_m19.90457942651027_5_impedance_speed_False.xml',
        '../data/results/m43.9653853242824_m19.9383851554445_m43.9252111325823_m19.899419689773328_6_impedance_speed_False.xml',
        '../data/results/m43.95697862558871_m19.940452374824503_m43.928999369322256_m19.904689345177896_7_impedance_speed_False.xml',
        '../data/results/m43.96044454229133_m19.935602569380528_m43.927486971404164_m19.902595967206803_8_impedance_speed_False.xml',
        '../data/results/m43.96307765908471_m19.936534694192257_m43.92878346604246_m19.90323786211238_9_impedance_speed_False.xml',
        '../data/results/m43.96378669575266_m19.937415550794487_m43.92556976074784_m19.90227285770205_10_impedance_speed_False.xml',
        '../data/results/m43.95842463867983_m19.93497835631086_m43.92129512514365_m19.90235042426268_11_impedance_speed_False.xml',
        '../data/results/m43.95808331863048_m19.936661310419854_m43.930358792315225_m19.89912528213961_12_impedance_speed_False.xml',
        '../data/results/m43.96446085632583_m19.937971076519364_m43.924723463485655_m19.902920711587992_13_impedance_speed_False.xml',
        '../data/results/m43.9612355417369_m19.941267713352413_m43.92984863384034_m19.898764680942477_14_impedance_speed_False.xml',
        '../data/results/m43.96495075153908_m19.942608827962108_m43.92911774818183_m19.899208956895738_15_impedance_speed_False.xml',
        '../data/results/m43.95784918158142_m19.93831108715641_m43.92615622459621_m19.89846196166522_16_impedance_speed_False.xml',
        '../data/results/m43.95937989265711_m19.936833980637793_m43.93219982725721_m19.89825689372424_17_impedance_speed_False.xml',
        '../data/results/m43.96293961431717_m19.935172607291324_m43.930357106881246_m19.903974461487174_18_impedance_speed_False.xml',
        '../data/results/m43.96034011898778_m19.93680839068091_m43.92662329614089_m19.901653732408676_19_impedance_speed_False.xml',
        '../data/results/m43.955235672746575_m19.93735112304128_m43.925528706428295_m19.904505533709262_20_impedance_speed_False.xml',
        '../data/results/m43.962508248386314_m19.939721380952662_m43.92870408013037_m19.905040976513124_21_impedance_speed_False.xml',
        '../data/results/m43.96118206717425_m19.937124071850626_m43.92794882222694_m19.90387030400352_22_impedance_speed_False.xml',
        '../data/results/m43.964235089598546_m19.935214304339706_m43.92487114842837_m19.902058670632513_23_impedance_speed_False.xml',
        '../data/results/m43.96388328437391_m19.941652310401462_m43.92827617311408_m19.903672220778653_24_impedance_speed_False.xml',
        '../data/results/m43.96242426308025_m19.93700754355518_m43.92727190816325_m19.904857644928587_25_impedance_speed_False.xml',
        '../data/results/m43.95965160072889_m19.940438581724024_m43.92715932553138_m19.9002848685454_26_impedance_speed_False.xml',
        '../data/results/m43.96790910414567_m19.935377000340775_m43.925772351210775_m19.90167005715351_27_impedance_speed_False.xml',
        '../data/results/m43.96312957554299_m19.941603786474108_m43.927559952832084_m19.904328777135394_28_impedance_speed_False.xml',
        '../data/results/m43.96118516288448_m19.940431956290915_m43.92455170562453_m19.902993970461896_29_impedance_speed_False.xml',
        '../data/results/m43.95994424010934_m19.935889252263795_m43.92718563643079_m19.902317407840307_30_impedance_speed_False.xml'

    ]

    files_d = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_speed_False.xml',
        '../data/results/m43.96258893392489_m19.93890742628848_m43.92910823112161_m19.902297290021462_1_distance_speed_False.xml',
        '../data/results/m43.96219206555545_m19.937592627268693_m43.92721201721954_m19.897338285624617_2_distance_speed_False.xml',
        '../data/results/m43.96515130388291_m19.933967721028743_m43.924803225217914_m19.901993293336044_3_distance_speed_False.xml',
        '../data/results/m43.958155756813724_m19.935767178008454_m43.925485937561184_m19.904408612118715_4_distance_speed_False.xml',
        '../data/results/m43.95818027059323_m19.938604532284597_m43.929235631948124_m19.90457942651027_5_distance_speed_False.xml',
        '../data/results/m43.9653853242824_m19.9383851554445_m43.9252111325823_m19.899419689773328_6_distance_speed_False.xml',
        '../data/results/m43.95697862558871_m19.940452374824503_m43.928999369322256_m19.904689345177896_7_distance_speed_False.xml',
        '../data/results/m43.96044454229133_m19.935602569380528_m43.927486971404164_m19.902595967206803_8_distance_speed_False.xml',
        '../data/results/m43.96307765908471_m19.936534694192257_m43.92878346604246_m19.90323786211238_9_distance_speed_False.xml',
        '../data/results/m43.96378669575266_m19.937415550794487_m43.92556976074784_m19.90227285770205_10_distance_speed_False.xml',
        '../data/results/m43.95842463867983_m19.93497835631086_m43.92129512514365_m19.90235042426268_11_distance_speed_False.xml',
        '../data/results/m43.95808331863048_m19.936661310419854_m43.930358792315225_m19.89912528213961_12_distance_speed_False.xml',
        '../data/results/m43.96446085632583_m19.937971076519364_m43.924723463485655_m19.902920711587992_13_distance_speed_False.xml',
        '../data/results/m43.9612355417369_m19.941267713352413_m43.92984863384034_m19.898764680942477_14_distance_speed_False.xml',
        '../data/results/m43.96495075153908_m19.942608827962108_m43.92911774818183_m19.899208956895738_15_distance_speed_False.xml',
        '../data/results/m43.95784918158142_m19.93831108715641_m43.92615622459621_m19.89846196166522_16_distance_speed_False.xml',
        '../data/results/m43.95937989265711_m19.936833980637793_m43.93219982725721_m19.89825689372424_17_distance_speed_False.xml',
        '../data/results/m43.96293961431717_m19.935172607291324_m43.930357106881246_m19.903974461487174_18_distance_speed_False.xml',
        '../data/results/m43.96034011898778_m19.93680839068091_m43.92662329614089_m19.901653732408676_19_distance_speed_False.xml',
        '../data/results/m43.955235672746575_m19.93735112304128_m43.925528706428295_m19.904505533709262_20_distance_speed_False.xml',
        '../data/results/m43.962508248386314_m19.939721380952662_m43.92870408013037_m19.905040976513124_21_distance_speed_False.xml',
        '../data/results/m43.96118206717425_m19.937124071850626_m43.92794882222694_m19.90387030400352_22_distance_speed_False.xml',
        '../data/results/m43.964235089598546_m19.935214304339706_m43.92487114842837_m19.902058670632513_23_distance_speed_False.xml',
        '../data/results/m43.96388328437391_m19.941652310401462_m43.92827617311408_m19.903672220778653_24_distance_speed_False.xml',
        '../data/results/m43.96242426308025_m19.93700754355518_m43.92727190816325_m19.904857644928587_25_distance_speed_False.xml',
        '../data/results/m43.95965160072889_m19.940438581724024_m43.92715932553138_m19.9002848685454_26_distance_speed_False.xml',
        '../data/results/m43.96790910414567_m19.935377000340775_m43.925772351210775_m19.90167005715351_27_distance_speed_False.xml',
        '../data/results/m43.96312957554299_m19.941603786474108_m43.927559952832084_m19.904328777135394_28_distance_speed_False.xml',
        '../data/results/m43.96118516288448_m19.940431956290915_m43.92455170562453_m19.902993970461896_29_distance_speed_False.xml',
        '../data/results/m43.95994424010934_m19.935889252263795_m43.92718563643079_m19.902317407840307_30_distance_speed_False.xml'
    ]

    files_b = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_weight_speed_False.xml',
        '../data/results/m48.48878893392489_m1.478707426288478_m48.455308231121606_m1.4420972900214621_1_weight_speed_False.xml',
        '../data/results/m48.488392065555445_m1.4773926272686893_m48.453412017219534_m1.4371382856246178_2_weight_speed_False.xml',
        '../data/results/m48.49135130388291_m1.4737677210287423_m48.45100322521791_m1.4417932933360444_3_weight_speed_False.xml',
        '../data/results/m48.48435575681372_m1.4755671780084498_m48.45168593756118_m1.444208612118715_4_weight_speed_False.xml',
        '../data/results/m48.48438027059323_m1.4784045322845922_m48.45543563194812_m1.444379426510272_5_weight_speed_False.xml',
        '../data/results/m48.4915853242824_m1.4781851554444976_m48.451411132582294_m1.4392196897733298_6_weight_speed_False.xml',
        '../data/results/m48.48317862558871_m1.4802523748244998_m48.45519936932225_m1.4444893451778955_7_weight_speed_False.xml',
        '../data/results/m48.48664454229132_m1.4754025693805244_m48.45368697140416_m1.442395967206804_8_weight_speed_False.xml',
        '../data/results/m48.489277659084706_m1.4763346941922537_m48.45498346604246_m1.44303786211238_9_weight_speed_False.xml',
        '../data/results/m48.489986695752656_m1.477215550794483_m48.45176976074784_m1.442072857702052_10_weight_speed_False.xml',
        '../data/results/m48.484624638679826_m1.4747783563108579_m48.44749512514365_m1.4421504242626793_11_weight_speed_False.xml',
        '../data/results/m48.484283318630474_m1.4764613104198503_m48.45655879231522_m1.438925282139611_12_weight_speed_False.xml',
        '../data/results/m48.490660856325825_m1.4777710765193601_m48.45092346348565_m1.442720711587991_13_weight_speed_False.xml',
        '../data/results/m48.48743554173689_m1.4810677133524104_m48.45604863384034_m1.438564680942477_14_weight_speed_False.xml',
        '../data/results/m48.491150751539074_m1.4824088279621037_m48.45531774818183_m1.439008956895738_15_weight_speed_False.xml',
        '../data/results/m48.48404918158142_m1.4781110871564067_m48.45235622459621_m1.43826196166522_16_weight_speed_False.xml',
        '../data/results/m48.48557989265711_m1.4766339806377888_m48.4583998272572_m1.4380568937242413_17_weight_speed_False.xml',
        '../data/results/m48.48913961431717_m1.4749726072913223_m48.45655710688124_m1.443774461487175_18_weight_speed_False.xml',
        '../data/results/m48.486540118987776_m1.4766083906809069_m48.452823296140885_m1.4414537324086771_19_weight_speed_False.xml',
        '../data/results/m48.48143567274657_m1.477151123041279_m48.45172870642829_m1.4443055337092632_20_weight_speed_False.xml',
        '../data/results/m48.48870824838631_m1.4795213809526584_m48.45490408013037_m1.4448409765131252_21_weight_speed_False.xml',
        '../data/results/m48.487382067174245_m1.4769240718506216_m48.454148822226934_m1.4436703040035197_22_weight_speed_False.xml',
        '../data/results/m48.49043508959854_m1.4750143043397042_m48.45107114842837_m1.4418586706325125_23_weight_speed_False.xml',
        '../data/results/m48.4900832843739_m1.4814523104014587_m48.454476173114074_m1.4434722207786517_24_weight_speed_False.xml',
        '../data/results/m48.48862426308025_m1.4768075435551749_m48.453471908163245_m1.4446576449285864_25_weight_speed_False.xml',
        '../data/results/m48.485851600728886_m1.4802385817240202_m48.45335932553137_m1.4400848685453995_26_weight_speed_False.xml',
        '../data/results/m48.494109104145664_m1.4751770003407731_m48.45197235121077_m1.4414700571535088_27_weight_speed_False.xml',
        '../data/results/m48.48932957554299_m1.4814037864741045_m48.45375995283208_m1.4441287771353941_28_weight_speed_False.xml',
        '../data/results/m48.48738516288448_m1.4802319562909116_m48.450751705624526_m1.4427939704618966_29_weight_speed_False.xml',
        '../data/results/m48.48614424010933_m1.4756892522637919_m48.45338563643079_m1.442117407840308_30_weight_speed_False.xml'
    ]

    files_i_b = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_impedance_speed_False.xml',
        '../data/results/m48.48878893392489_m1.478707426288478_m48.455308231121606_m1.4420972900214621_1_impedance_speed_False.xml',
        '../data/results/m48.488392065555445_m1.4773926272686893_m48.453412017219534_m1.4371382856246178_2_impedance_speed_False.xml',
        '../data/results/m48.49135130388291_m1.4737677210287423_m48.45100322521791_m1.4417932933360444_3_impedance_speed_False.xml',
        '../data/results/m48.48435575681372_m1.4755671780084498_m48.45168593756118_m1.444208612118715_4_impedance_speed_False.xml',
        '../data/results/m48.48438027059323_m1.4784045322845922_m48.45543563194812_m1.444379426510272_5_impedance_speed_False.xml',
        '../data/results/m48.4915853242824_m1.4781851554444976_m48.451411132582294_m1.4392196897733298_6_impedance_speed_False.xml',
        '../data/results/m48.48317862558871_m1.4802523748244998_m48.45519936932225_m1.4444893451778955_7_impedance_speed_False.xml',
        '../data/results/m48.48664454229132_m1.4754025693805244_m48.45368697140416_m1.442395967206804_8_impedance_speed_False.xml',
        '../data/results/m48.489277659084706_m1.4763346941922537_m48.45498346604246_m1.44303786211238_9_impedance_speed_False.xml',
        '../data/results/m48.489986695752656_m1.477215550794483_m48.45176976074784_m1.442072857702052_10_impedance_speed_False.xml',
        '../data/results/m48.484624638679826_m1.4747783563108579_m48.44749512514365_m1.4421504242626793_11_impedance_speed_False.xml',
        '../data/results/m48.484283318630474_m1.4764613104198503_m48.45655879231522_m1.438925282139611_12_impedance_speed_False.xml',
        '../data/results/m48.490660856325825_m1.4777710765193601_m48.45092346348565_m1.442720711587991_13_impedance_speed_False.xml',
        '../data/results/m48.48743554173689_m1.4810677133524104_m48.45604863384034_m1.438564680942477_14_impedance_speed_False.xml',
        '../data/results/m48.491150751539074_m1.4824088279621037_m48.45531774818183_m1.439008956895738_15_impedance_speed_False.xml',
        '../data/results/m48.48404918158142_m1.4781110871564067_m48.45235622459621_m1.43826196166522_16_impedance_speed_False.xml',
        '../data/results/m48.48557989265711_m1.4766339806377888_m48.4583998272572_m1.4380568937242413_17_impedance_speed_False.xml',
        '../data/results/m48.48913961431717_m1.4749726072913223_m48.45655710688124_m1.443774461487175_18_impedance_speed_False.xml',
        '../data/results/m48.486540118987776_m1.4766083906809069_m48.452823296140885_m1.4414537324086771_19_impedance_speed_False.xml',
        '../data/results/m48.48143567274657_m1.477151123041279_m48.45172870642829_m1.4443055337092632_20_impedance_speed_False.xml',
        '../data/results/m48.48870824838631_m1.4795213809526584_m48.45490408013037_m1.4448409765131252_21_impedance_speed_False.xml',
        '../data/results/m48.487382067174245_m1.4769240718506216_m48.454148822226934_m1.4436703040035197_22_impedance_speed_False.xml',
        '../data/results/m48.49043508959854_m1.4750143043397042_m48.45107114842837_m1.4418586706325125_23_impedance_speed_False.xml',
        '../data/results/m48.4900832843739_m1.4814523104014587_m48.454476173114074_m1.4434722207786517_24_impedance_speed_False.xml',
        '../data/results/m48.48862426308025_m1.4768075435551749_m48.453471908163245_m1.4446576449285864_25_impedance_speed_False.xml',
        '../data/results/m48.485851600728886_m1.4802385817240202_m48.45335932553137_m1.4400848685453995_26_impedance_speed_False.xml',
        '../data/results/m48.494109104145664_m1.4751770003407731_m48.45197235121077_m1.4414700571535088_27_impedance_speed_False.xml',
        '../data/results/m48.48932957554299_m1.4814037864741045_m48.45375995283208_m1.4441287771353941_28_impedance_speed_False.xml',
        '../data/results/m48.48738516288448_m1.4802319562909116_m48.450751705624526_m1.4427939704618966_29_impedance_speed_False.xml',
        '../data/results/m48.48614424010933_m1.4756892522637919_m48.45338563643079_m1.442117407840308_30_impedance_speed_False.xml'
    ]

    files_d_b = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_distance_speed_False.xml',
        '../data/results/m48.48878893392489_m1.478707426288478_m48.455308231121606_m1.4420972900214621_1_distance_speed_False.xml',
        '../data/results/m48.488392065555445_m1.4773926272686893_m48.453412017219534_m1.4371382856246178_2_distance_speed_False.xml',
        '../data/results/m48.49135130388291_m1.4737677210287423_m48.45100322521791_m1.4417932933360444_3_distance_speed_False.xml',
        '../data/results/m48.48435575681372_m1.4755671780084498_m48.45168593756118_m1.444208612118715_4_distance_speed_False.xml',
        '../data/results/m48.48438027059323_m1.4784045322845922_m48.45543563194812_m1.444379426510272_5_distance_speed_False.xml',
        '../data/results/m48.4915853242824_m1.4781851554444976_m48.451411132582294_m1.4392196897733298_6_distance_speed_False.xml',
        '../data/results/m48.48317862558871_m1.4802523748244998_m48.45519936932225_m1.4444893451778955_7_distance_speed_False.xml',
        '../data/results/m48.48664454229132_m1.4754025693805244_m48.45368697140416_m1.442395967206804_8_distance_speed_False.xml',
        '../data/results/m48.489277659084706_m1.4763346941922537_m48.45498346604246_m1.44303786211238_9_distance_speed_False.xml',
        '../data/results/m48.489986695752656_m1.477215550794483_m48.45176976074784_m1.442072857702052_10_distance_speed_False.xml',
        '../data/results/m48.484624638679826_m1.4747783563108579_m48.44749512514365_m1.4421504242626793_11_distance_speed_False.xml',
        '../data/results/m48.484283318630474_m1.4764613104198503_m48.45655879231522_m1.438925282139611_12_distance_speed_False.xml',
        '../data/results/m48.490660856325825_m1.4777710765193601_m48.45092346348565_m1.442720711587991_13_distance_speed_False.xml',
        '../data/results/m48.48743554173689_m1.4810677133524104_m48.45604863384034_m1.438564680942477_14_distance_speed_False.xml',
        '../data/results/m48.491150751539074_m1.4824088279621037_m48.45531774818183_m1.439008956895738_15_distance_speed_False.xml',
        '../data/results/m48.48404918158142_m1.4781110871564067_m48.45235622459621_m1.43826196166522_16_distance_speed_False.xml',
        '../data/results/m48.48557989265711_m1.4766339806377888_m48.4583998272572_m1.4380568937242413_17_distance_speed_False.xml',
        '../data/results/m48.48913961431717_m1.4749726072913223_m48.45655710688124_m1.443774461487175_18_distance_speed_False.xml',
        '../data/results/m48.486540118987776_m1.4766083906809069_m48.452823296140885_m1.4414537324086771_19_distance_speed_False.xml',
        '../data/results/m48.48143567274657_m1.477151123041279_m48.45172870642829_m1.4443055337092632_20_distance_speed_False.xml',
        '../data/results/m48.48870824838631_m1.4795213809526584_m48.45490408013037_m1.4448409765131252_21_distance_speed_False.xml',
        '../data/results/m48.487382067174245_m1.4769240718506216_m48.454148822226934_m1.4436703040035197_22_distance_speed_False.xml',
        '../data/results/m48.49043508959854_m1.4750143043397042_m48.45107114842837_m1.4418586706325125_23_distance_speed_False.xml',
        '../data/results/m48.4900832843739_m1.4814523104014587_m48.454476173114074_m1.4434722207786517_24_distance_speed_False.xml',
        '../data/results/m48.48862426308025_m1.4768075435551749_m48.453471908163245_m1.4446576449285864_25_distance_speed_False.xml',
        '../data/results/m48.485851600728886_m1.4802385817240202_m48.45335932553137_m1.4400848685453995_26_distance_speed_False.xml',
        '../data/results/m48.494109104145664_m1.4751770003407731_m48.45197235121077_m1.4414700571535088_27_distance_speed_False.xml',
        '../data/results/m48.48932957554299_m1.4814037864741045_m48.45375995283208_m1.4441287771353941_28_distance_speed_False.xml',
        '../data/results/m48.48738516288448_m1.4802319562909116_m48.450751705624526_m1.4427939704618966_29_distance_speed_False.xml',
        '../data/results/m48.48614424010933_m1.4756892522637919_m48.45338563643079_m1.442117407840308_30_distance_speed_False.xml'
    ]

    values_t = []
    values_i = []
    values_d = []

    values_t_b = []
    values_i_b = []
    values_d_b = []

    for a in range(len(files)):

        file = minidom.parse(files[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_t.append(duration[0] / 1000)

        file = minidom.parse(files_i[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_i.append(duration[0] / 1000)
        # 1, 13

        file = minidom.parse(files_d[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_d.append(duration[0] / 1000)

        file = minidom.parse(files_b[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_t_b.append(duration[0] / 1000)

        file = minidom.parse(files_i_b[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_i_b.append(duration[0] / 1000)

        file = minidom.parse(files_d_b[a])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        values_d_b.append(duration[0] / 1000)

    m, h = mean_confidence_interval(values_t, 0.95)
    m1, h1 = mean_confidence_interval(values_i, 0.95)
    m2, h2 = mean_confidence_interval(values_d, 0.95)

    m_b, h_b = mean_confidence_interval(values_t_b, 0.95)
    m1_b, h1_b = mean_confidence_interval(values_i_b, 0.95)
    m2_b, h2_b = mean_confidence_interval(values_d_b, 0.95)

    medias = [m, m1, m2]
    erros = [h, h1, h2]

    medias_b = [m_b, m1_b, m2_b]
    erros_b = [h_b, h1_b, h2_b]

    print("medias, BH", medias)
    print("medias, Belem", medias_b)
    print(erros, erros_b)

    # define sample data
    # data = values  # [12, 12, 13, 13, 15, 16, 17, 22, 23, 25, 26, 27, 28, 28, 29]

    # create 95% confidence interval for population mean weight
    # print(st.t.interval(alpha=0.95, df=len(data) - 1, loc=np.mean(data), scale=st.sem(data)))

    labels = ['PMT', 'PMI', 'PMD']

    x = np.arange(len(labels))  # the label locations
    width = 0.25  # 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, medias, width, yerr=erros, label='Belo Horizonte', zorder=10)
    r2 = ax.bar(x + width / 2, medias_b, width, yerr=erros_b, label='Belém', zorder=10)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # ax.set_ylabel('Potência média (W)', fontdict='bold')
    plt.ylabel('Tempo (h)', fontweight="bold")
    plt.ylim(0, max(medias) + 2)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(numpoints=1, loc="upper left", ncol=2)

    fig.tight_layout()

    plt.show()


def plot_all_length_BH():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_speed_False.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_speed_False.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_speed_False.xml'
    ]

    times = []
    for i in range(len(files_result)):
        file = minidom.parse(files_result[i])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        print(i, duration)
        times.append(duration[0])

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [times[0]/1000,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [times[3] / 1000,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.errorbar([1.325],
           [times[1]/1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           yerr='1',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [times[4] / 1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [times[2]/1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [times[5] / 1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Distância percorrida (km)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()

def plot_all_length_Belem_2():

    files_result = [
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight_speed_True',
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance_speed_True',
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_distance_speed_True',
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight_speed_False',
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance_speed_False',
        '../data/results/oficial/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_distance_speed_False'
    ]

    values = []
    for i in range(len(files_result)):
        dados = dict(Graphs.open_file(files_result[i]))
        print(i, float(dados.get('total_length')))
        values.append(float(dados.get('total_length')) / 1000)

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [values[0]/1000,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [values[3] / 1000,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [values[1]/1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [values[4] / 1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [values[2]/1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [values[5] / 1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Distância percorrida (km)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_all_length_BH_2():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_False'
    ]

    values = []
    for i in range(len(files_result)):
        dados = dict(Graphs.open_file(files_result[i]))
        print(i, float(dados.get('total_length')))
        values.append(float(dados.get('total_length')) / 1000)

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [values[0]/1000,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [values[3] / 1000,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [values[1]/1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [values[4] / 1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [values[2]/1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [values[5] / 1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Distância percorrida (km)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


if __name__ == '__main__':
    #plot_all_length_BH()
    plot_dist()
    #plot_all_length_Belem_2()
    # https://www.tablesgenerator.com/#