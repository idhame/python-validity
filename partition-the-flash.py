
from db97 import *
from tls97 import *
from hashlib import sha256
from struct import pack
from usb97 import *
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.curve import P256
from fastecdsa.ecdsa import sign
from fastecdsa.point import Point
from fastecdsa.keys import gen_private_key, get_public_key
from util import assert_status

flash_layout_hardcoded=[
    #      id ?? acc  offset   size
    unhex('01 04 0700 00100000 00100000'), # cert store
    unhex('02 01 0200 00200000 00e00300'), # code
    unhex('05 05 0300 00000400 00800000'), # ???
    unhex('06 06 0300 00800400 00800000'), # calibration data
    unhex('04 03 0500 00000500 00000300'), # template database
]

enable_blob=unhex('''
06020000013920c0cdd8e7e68d6ef897ee686fbf657f83b9514341e1d3c0835a28c9cd1ccd0016644f74d
d02a73b85d95f4d352417cee76ba0bca3ce474159c62ade3e10797715a13f15a292f5d57c6d46cf8f5ef6
587a3c55244f2258ffd08b351dc14af0da36121ba0aa4f1147ffd0cccdc1d6dc1d5fa7adb9841ff79c753
e2528dc27344be84a2655ab01039c74999b90a7f008f626791d68a76a57b07180129bad2c0a67daf6a3a5
ebadd6a429fc087b1e68f1e6535290b7f94e9a9800330d866c5a67b4e974029164f8c6fca8d93c86211ac
47d96fe386faf206f92f4afd32d3a90c4287377e8896aa9ae930543864539df833345d0a1869169d69100
8510c91dc1a0ec138669c2efb812c7b9b7f201891cdebe9c80eb671ac8a854bdcb9990cc23950f9f1dda0
d0119b8c5c2d8446310e8599efd248075bad6613ceb13f0310ceab6ad17b18c8a245c26363ba7a7f24f17
972861c6a96e728d1be81a68d66418ee2dbdc00d240bde29c781069f93a06dff89ba4039b980d3c9c2a26
a7f41a02a4b9f1c0e0f75f0a59c5c5003d2e90a209cd9f8bdf69414262e238dbe8e1bacf6c880f59843dd
8111293e24e99c964538842dcb0b4a8cab6d227cbfe0647cea763496425152aed507b2228e79c8e9bcaaf
6380c1d2e7f56c5563706cb5da5b238371ca4b2627ca00f9bc9d71cd73ccf02f02f42e856f9e8defa0195
c8647cb1a0a63e6996a1b5906080851f1648cd061a585ddda05fc8f37a99a0dac92dfabbfade8f89157cf
11d356782689838c358f4790480fd341c993ae4cc8a8c93cf11578c0571e0c3c8a4964286eac3fae27507
d9fb2ee961953d86574e6e5f6d38cf2507a714adbc221867bd701bdffae0b27ce47ae8d06685e534342d1
1aef07f2c998fffe8673c2806e8384738b8f4ba401d417cabe088ed2fa09c42e97af72f878753ffc50b87
fd292662f421bc6cc8da131957c84f4ce4b69266065d35d3ab91362b13edac27231ea1b6485faa6644c64
6747b86341b6d031f6a52b6ad855396b7b8cf9485f50365cdce203355bf2fceebfa59b266772ff2578bb5
03f92ca35ca2bc046d63aeb4fbb0f477ef41c65d10c5cdcff5de10afa9e7bc08b026f0fa649629f259c5c
2978d26dfc2cbf48f59616ada4bf2fc7a7219fc37d9f5026709e7b472b6f97f78d47e1c5a6af8e23aebb8
a88f64f005abc93251aeb8561b0d855941b33ac608413405381fecd0154db93812843f15b8e5e118ba7a7
cdc051ef203a7721b769abb3c17c704eb0acf6a2cde267776dfb1ff8d82ba2341d0346cd80cd4480767a3
d0edb643c1d9045f24096bd1fc324c03efc0977736725b2770998ea920c19a1fa9add474714a5b7a2a318
7e94cf1a3492814ad145a7b204e0b3d35dc4cab2424a891f76160ba722a25bf9906bb3a476250b756249c
aed3c4d52c4046012da280ec71898e8e393559979a74432f1df2692616c761c676a0260c7e4042bba7387
d3c683d4e08454c7f509b7960a1db2a1cf007538a38a1e39b0a0310c9b77fbf21ab2b3f2e76f3ec9084c6
f47f4fb2fc1dbcab40a9d1f6c8e404126193d26ed98270824611c4840087893b3204837e282bf29623080
439336435e801de053cebb066bc7a440a3f34fafc2bb7252c5dd846af3404e93f1172ebe2b7861e09d58b
cbee0400df8fe627adc42be2860a33d40748bab2f34262ee32409bced9cf8fea90bc32d247dc2787d7289
65373063851a991c63c480b67cd301a9c312037c72ffc04120a09b1413756d4e5bb0bccb550c6cf76e2c6
35c8498f4e653beee2fb683db0466280bbd297838a8d1f2459a58db77446020cd20b82a52ee5cbf0aa908
14a199ae61dca69d0bc90986a2c26b8d65357e3925774a3876ed0eb80124a0bed4c2c0bc632e1b3c1a812
2b54b023b05e846d78172b97424ff607b67c2c11f21ceadf82020129e62fb0918e85b623134f4e5e18870
42b632662a3d33c6effa4a967e09a4d988dd084fde8c9d4b39dd0e6521b8e2d376807adbb5b86d914eca2
38a349d9b0fb23b64668bdfd45f6a735523a31878e4975a42ebe2d3c920f550881818c8139cda34df3669
b89aa5fc8b3bad460de2d76d431435c83b6fc0efbaaaa84818e990be36b72826f00f1f2b97d63b680d83d
03f2ac5325f8dfc5d460abcbf27ed4ff205542702974eb9bfba456401786578efd93d69ec76a41df43798
76891e39acdce7a32e94811157d48829f46b5755d9721d935c73a28423080bc8a48882b4439e92ac68413
6a52b078e06a730596eacab8768d0784b0fca63f8a247f2523ea5d4679a8957af6b314594681759ede769
76937c5f99c7fc9326579d90fe7a7fe0d512858e3221b50c4e1d9ff16f38d49c52a524ef895dab24059ac
7a2b9dc24e59d8b38e4958d51fc309deecf987dd79697fe6ccf955e06bbd0ebe69aa18df39b452ff9ebe8
f2f761c1be272141ebe65d0a625b5f1398ac2ae129ee5c1e520beeb492748f9364742978249470be45279
11bd9aafbcbfa5e90a56ce40e42b995c82f6c5df51cfedc41a6963475e2d39641e2d7ac624d184aaec303
465d4441b1b0acfccf9b45cc3e1825a01be94e93ee16918793a809cef222480377558ee18bc2801e31f24
3d609ead015a0a6cec743f7dd0d951a7e0bf56d45ef20177373972602417024412c2adef44b881da42138
5286c9e31fcf98b8f8ee10a9ee2730429579825ac159bdee29d1c4cdb9073427d0924174d04818b6586d2
d2ac5318156b6139bec3b1959d0d1a8b46603f0ae9862214fff30c133d463cdabf875ef841e01976ad06c
bf74c9987839e8a0e41b6a2411e542a061b23bf5b261df7a0cc844c510c102b4e03fbc44c44e998a51699
907d252e91e3e89c0728f5db0b868ff2c55fc53d9230dd0dcd01086379a8821a0cb2b7dfb90b25a8c452f
285185457827dea2f5b3cf1138e23e9a8d23ba1f2234d233c0c7f0595471e7e3a62d8fbb8a5fb900a3cf0
3ee4943e4a4ba5b51200f02a6217ec29d7d5177ba395c77540b7111c5428ab069613c7e17094c5d798049
3ce2d945393f3fc11765629597817499cf6585635a3db8d6471af509380224dc04b574891ebce80cb7ea4
d0789ffd7b76637fd460ee701b60be9174eeb51f96c6811a4e4dc55ee545a9d9d23b80059084616521742
d9b7a47d60b77dd0ed12f10327553448655ed7b7a9d7366854d908a4c762fe9048e4e4a3776f2e22f90de
014643101de4715754efd62762500c6de90435fcde78e9fb864045cf8749b93907baeb4f47230547e78be
a0e01d918426c3c7a3bdbbf2b54394c44273aaf163306450505862af4778f667d7c34a894c8824effe124
b9993690d1519015566849652d86e158830465fd1fab08e4cf5cfff1f437ae0c713abe1b8e1fd15b1a796
3751504ea02e4ff1469300a689d4ca4d796be229b4cc041296f9672bb2383442d492eaee0a17d174ac699
4d2c1b1a117e54da2bef43347129d94bf4ea029271564f05fc3f607bac5e06e741ed5e9d51a2efafec05d
7926c693bed05ee0bc81c1b6aa6d57f58b01aad2d69613c201e86312bdd2e8117eded970e298c096c52ae
d21fd7f8aa03e3bf3d280fe3b3ca4e49dbfc90dbdfcae59ba03eb38458cd01f6637843526881b8df0b019
e90e2b05bb4154dbac69e82ef4d8f83343fa2b0f10f71f1f0c314f41ca366c296fc41830ab1998829cf55
01d8afa090b8803aa1ef94dc8a06c231ebb3e42cabaedc50fdc40832091307b4dc46398c890d71863522a
927e1d90cb72d38afbc74ffe8813ab36a168822b5caf7550af92824061d076b5e1f628b6e4a36849c5182
58905e734a2dd53258df37305a16c0b844dec711800a822dbf691327b7fac815cef33d59363d56c246d04
e877ba09c4fc1aa70937d46adea4b1ba418695a7b86c0d9332b71d44b2dd8c88c93a8efc264b1c29820bb
5b66b397136d9715961dbf7d5b59508015b2938edb1938e68f4e354eb7dd60b08b4460c05d1f291e56aca
32bf30a59b1d849993750498df7be8101d38cb2781cb52a640dfd09ad469bdaa069eb37b7462343819ce2
024bcdd1940f97eec044f7fe41793fda6edf53acc92d2883fdb144de0baa6fff19c59b3b5a673a6be202d
8afb436fc6bcf3a5bce2ec9919a9d2f4aafcf2f83698d56fa43efa7b07fd1074b915344d6ce24ffdea58e
b3afd95d911187b1070cf1c97a80ec5a5d609869e262b347f24b7e33404e6daa06c89d45db644cc6e29df
41198bc8ef699415629b91b6ba52e5cccfc367654ba4fc0c7c6f40a2d9ce519c84a6315dc6e951f828b1f
5d3a7c6e7e4a3271dc21c82329a163315a763c25710dbc33f9b79db33eeeaecfb8345d503fdb069160451
67cd5451c5feb5358b07b085cb710f348150c92948aef7eca1bf4f51cb31b7429d28ad544cfd325691524
ea5a13fb276967ff78719eae6c735d37d7206ba951cf115210ee0c3a0b07268c57a926a4ef8dbd8423190
8d15ca9a2f1b519ee982a539eea6e874a6b04cbb65c62ceeb44d7ccf14791bdf5f056bae592830688f03a
67d92a8b6b8ab6c40c651eb4e2366fb31434475068839466fff8e5279cbafa713b8d51dcf68001363dad4
ac42946ebd79493fca1a868398063193b4f0aca3a5af2fabf868813b91f8f13ebff3430d31ea0d4f43ed3
f4b620cd555e685d4ada88cd1df2dc108e1c6202531b63deeb47fc56cf5034a31f6009dbc21ba392464ce
c0f410756705d402dc05572236c291eca7f2de1315b9d120f5e90272d2643ee4f941b387b3dda516de4a9
a09b3407ceceb015206edd6ef6449fd3304fca2f306e455c6daee470edb19732b76c1982ca03e325d8563
c7531abdbe99e8a7742a9802afe43bc46fd795d46052b527d1125f65427c60e6bbfe5e4d391c391a62118
ae1ce651622ea9f2a6f4f6a57271b35bc907ded5ee7026adc8f77f50168b75741984e9cc788acc8ff4de7
a1aa976466a45948d8b40e3a9ce32ecae381c3376692012456b76ff9b58d70b277e564a2edae34b459476
08e660eed03c3d2f4f7112a0bc7b9628d86694f8dd1fb5d9ad8c62c957c1640aad6d0106b1c9d089cfd1c
30f155a1e84a2a809f08e212b8b06a81543f2fbded09620782bf8e2bc70461b45a567727c74c1703a23b2
3d3014db6a05a368ff9acc84d4fde73f1763603bdcd899b61cb3bcebb900268c93fbd0f12f702661d7582
b188ae01922c95dce32d0469e30386774afcf89e4f107a949ba6dedd17d828e480ac653c07ea30f780879
be572bdad635c0f9f87d88360b5023e58b661f35df98b7b1a0b1779179e614281147d9c6a4f0853e4d435
432b4d6be3879315e2c4fce0ba32a9be43fac22b4f12a97caeba8ba4770c89447dbd902287ffabfa3d270
64a45060a2fa458e950f34569ca4cbfdee9b3ff6391bc5a0903e66f5b99526fe75c10a8ab4fa9a100948d
71ab96d51e3076e84ac00460eb493b418130f6ff92c0c0a2bba39a14b3f5f003583f481abf35d39dba4ef
e41712a6eb1f8021f18d206993c685d806a8c8415cbbc15332ceabeaa8d8f0de9af037c1128fa0207ae5e
915c79276e23252fa8255448feb00d79931948967db93f8c95336237761d2eb9cde0eb3ddbf2b0e698136
7ac6c5843902670a5bb3a7fb3cc338f7b498cc07db6454e7c8c9b2035e1e21fb1046693a39fe27fc04a38
0a209c7ce67c238bb227a9bee07407a9fe65b0914976af513ed2f9964574bf24162940269f8e34d6fed0c
0769c81a5dd890e2b7d92c4ad51126ec8158679fa5c014428d67e485fdcdbe24e9a8f7bd46ad3b02354ed
febc7133cf198a841a163a6580ad89badaee7620419e30234ca94744d936bad9ffa468bcf669741fadb7e
7da12908e4903eba485cde036725fc4ffaef6e7a1500f40428418ef570b355810ba4981fdfb039b4e5d84
50e979ab8f676d1b1c84897fc5cd7ed57e4962686a91687f04932f690ad55a85a7f235ea99d3ee0ee9a8d
5ef0e84d43c2ec8ef3b3da80a5c3c973e41e6d85cfa28f53c3cce3117b05662f23f8f37923518a77e5408
76abb03b6b1bdd606ee9127ed6c03a8b90a30e772ae9fdd287cff1df87d2ca3b344f615afdccf09f9aae6
115fb99b7a4da857c30d73e08c7cb474a65564536738f64630013e6e7a375ef2b721ceeb77c2bee0be730
5f4beaf9fd048ccc03e2a536e57afe06cb981b8d788c0114b1422ccd025205a92d1d98b7de5f604e3e55e
2621f2d8933169615c9e5a6f354396e184ab69722b33eace77fde03c67b553084dbd35ca860f8e1798827
9539eda36bf63bf8b1345491ced4c6c89ddcd709ddecc764a86565b8ba49368c4a4034302acfc0184c3c2
d9f8ba34fde40cef6d3869fe6a5d1af17e059445d3bf9c950470cdac062e2986877ec72a79333089b2ce6
9ffab8c5438a1298bc50e0e9c2e286e55b1936ab0903257d52db14fedeeb67da7a1df1506b0fdc4a50d2c
721450150b25fe8cb74c39298f620c029dd8a9f1f9b175c5083a6437d0a8f5d05489aa2ff31dfc8ed83aa
dbee192b11169e3dd6bd496eacc42c46a952f81f8c39f88ba31ec08f1060d2f2e49c0b900508b4e9e5703
003099bc9485e09e5c6a8c9f05389124095b1c9693a30e4b75b7f2e839eb252237a55007ac61fb5268982
083d29e757b74c4c310aa1cb03adcafe17afd50a53e4f539fb57a6c5c93ee94cabf36d2375cf0d99ad0dc
cabb650f468737745cd0d5e66ca991bfdb46e05371bfa18a034669e967192a53bffce26bf2619a365c21f
9f7c54801780c12ad3ff7198e916a1a4451bdcb248aa997d25f312a292c9ae1f70efa6ef1e5df24e48cb4
1243ccbee736dc9d32476506126500906db396f312db3d6710669064711709597220dc3367e720819105a
f78bfc5a109571b763f44873f4b820af8279d42bff9b5f9da409e0ecb9d6a3485d9bbaf2641461c1cf144
eaa2cada36b38beaec87737dd70158735bb9c0ae7de4ddbed353411b8435c80cb2e66a701469c6e65f437
1d114775c73d8bfa0ca04b38811b2b31261b86dc2795388577376501aad9658c630d7ac9fa4c1f262d53a
91cef7c2990d9597fb2a130985e04233cf178c611be685623ffe5b659af6aad10da3235331fc6f6822fd5
cdad3f96e3e1195bcb3c0104ffacf940b570f94ae689924cbba86521af15be9b1148f331ddfa37ad410b8
ef99979a56ef1c3c789ffb996507d85383559a229493ad0bab90478d123f0c577ef01c5dc5a3ea28f60d0
8409544ea6e44724240b2879f9c2560270e0cc3949af9e22899377635f44cc3fd0120554503d06f4a2b41
e42129e7184265b4480edd5031d57368789203fb9a666c1be6692451f684119d85ed4cd88fe63dc1d16fd
dc4b8508d04671f837f413a653483f0eee7b5300021735de246ee24d462c5d332c55d4c35c1ab9bd7c9a3
d009076a838baa8a88c6fce72f0805ed73221fe98a5941d21a97ab5641d2e54df83c2437fa9cd88dec024
1f1254c6a0ca3e85f678eafab8b013459590f87fd580fc0c05f5967a58f4dfe6a89ac1e47e4dc09adc942
4336dd355c6f783c2698b8539c3f801f999ce5db3f041cca86b75e3e92e3d98922ef2c191282a7516024d
f2949c1e88ea6b53b5d713b57d3edd5c78a978f7d854e487eddc60c7685120980a5cdc259cfb2de591875
d88f9b898ef60d6da810b1a07252a56993bb5bba723f4f838ec648e19bf63dedb33eb1dbf07f456b41563
c0102cb18220b308ef60908e75a77e6954a4f2993b60c10464dafb40e79e3cf5dce392207e473913e61e2
75b090793fe0bc1856b6574cbc6fd1295448b34caa325df832a095266beec91604a2726f33e54e25e9478
d859c348ad45ba5b51eda93cba7d957c5d0d76f2de84d225a5cbe6a5553c1311c35f12281d98acc7eec95
d7f5e0ff3a0b27c0032b59a656f70d0cc5a042ee5b72365c0c8ee03ab6c48e18f87e050fd9707104924c1
59b48edafc57cbb56722f62702390e688a0bd463c95318d3bb13b44033ea78d19c665aea20c67cd7896ff
cf2c8e2806e5380f0d53b0b8d30fdb35d496a891dab54d3a4ab1b2a6f4b4091b48b339c5213a6f8c3f8ab
9a9873a605494cedf22b17a6defb8ec1a88f471ce7c073ce264fffcf9af0c6a37398491652fae2c29a496
6b022fe608c51f28503dcced1d5961186c3889e4d5ea8bc94667c80cf0d6b5f4ccf3d8addbf56b6c78028
0850e078f39d2377376e120ad05e930e1c58f50bcf980814c2e38215db50567c8870bdfa9940104591384
55fdbb2e260190dfac1743a5d6dc9031b0c89bfeed9f70ffa84a964a185834b4e2d3f299f2c4fea605f4a
5a97c51fcc0fad21ead2867dcb8fb6cd6ae2ae271e89477d7dd03c34508d719a037fca0c6cb028112d8be
93fa865ba60c7d7e1e017f3f49a9f0114c6fab8fe797cc3a4cc80c2351880347ebd8288895fc210431c8d
27ef350588a81c382de3a100f8f8458eebb61e33336b179ae24e397661d622c82169c1081fdb929b9f21b
4410a09fab9938c40573757d89a4450a4246deadfe4e5a20f04b6162f06bb0ca4c658a88880df139a5641
350edf1d19123cce164d5760b6806ba8ec5584effbb87cd284150ed6a73354f9829f5d22508da40bf8f9c
7351c45cf169a3f4e7354faed2f42d9cc08ce051e902f8137a8f79b924e2b3000ed25154e617b5d066ff1
a3540eed0a4a3da0618d961115091a6ad9f831c25e2ec9fb1ddfa3c28f365b608fa1dafbb0ba9fe340014
60e6af2c2da1e90aedcfb07da4e6603a9879834f16fa45cbe6c2206459058c750e534dfb8fefba9bb473d
0f307f2e746f4c4f6f7db41bdcc7eb5d7e4c9d5028ce143cd88ebc1efa56f0e9f3ef939526a3f56ae015b
5e42fcb7353f5496cb70baf316c8b1bfc7f26872de3f421e87ac81d4a2f51b6c44dce38a6dc9d93009490
d84d81807e517f06c896f8adbaac3d5d8d8b83b220114d0da49dffbc5e2cd1e2b715e671b05aa1fd3b0bc
dfdad56f65d0393dd9d1fa384b82ccf9b10b36d929f6b8e433999448f23c6c228bff904c0b91d0490af31
3623a76fcc4258e9c8efa7ceb4b82aa0cfc6c362eac5b1e61f2a55ec5d3f401a748acb6b8f2dc4641ef9b
d4eaf3d20e399956d36c338902c5e3b7ad13249b03bf248f41bb26de70db4d0b0b4c8dd51f92b5c1e9f3c
cc7cb4ae36945a16f6b428caed3514af83885312a6e176d9c555199cf7cf444915362184d82d21538697b
10326d0c5bb1e99b44ad644de25edbdd2ba404a45258d0e1682e73a42595b797f5e7a0f8b24159047d98d
8fc58ee9e47a5068d791bafecee6422d7bc847757c0800c95e23f3470f41500bc08ab71d671765cda7422
7535ba05696c703b90ddaaa6e6973389abbea81600e36229d756f7edcc1aceaaa010f1c5aaa1e6f0def4e
b3a04613ce82527a67f8be50d072cbca685922d492df81cf737a69e29bb4248076464ac3fbe88db35864e
69b71d1ed5b83f2045f680d9cc5d447f09e5405a5939943511eac648c10aca735209612eab589d2d2716a
19059248ce4847f3a809ff04477b8378da77e796109fef7d686a5f067cf3d91aab97bd518f388173d9535
26a3a77af043427bc2b2a466735a45846c11204b56a84394d724511efb467722ffde80899d3868a31c7ce
4c8c2100bcab717f12eea1eb11a7f28abadbc819ceef1132a57f902aabd43337172b3aec8fc7577bca293
50551070615735499b2758b2d9c77d391497393b6ad39e3395834185a76f6ce93fca5376e6f5aa78b11a7
63f504781ae3e8a773c91e3899574c4b3bb0221ce8a927d443d5292f3ad13e843146736f457b4477ba6d8
f462505b7d3d0fa76dff52f01924e00df97944f69a3abe6564793bba2850b0084e4f8d2ace474a1249daf
1a4ffdd4a8df84c8d5ead6909929992ca1b6e58476ff388bf978d091921dda2db3b1121e573eee682e22c
d01818ae0b7347e2591dedf20ac857746b82c0d4498744744ccb44ff96857a9609d7a500f243a62106e61
8eadffeb5355d5e5e7452f5f50b3de48e75adc2be249b20ccc4aa3f4ea357bf4320d8f42e5a3bad1bd3e4
2c659f71caa3736871f9b95887adbc04affecf1076598d898917c0b54c63317478b8b8e65fa2e6b243d7d
497cebfef615c9974553feb3d33289577886697b6fb01a8849d4714ddf9688080fb0af0e6fcba733b8019
28e7664b3840a02b9aab6307af1dd3fa814045733b53e0adab1ec430c40e184db1ceca1bbd58c4dab244f
8683bd4edb6e59470deedebe96080be666b779106de5d6acef113a6c75002424e4812e2d9997dec5391d3
aaba00320314f44fac9e7ca9b8996bd0a61b00139a8c1d2c9fc52e6ab9f90eba248ab0b3c4444d4ad1f07
ac36878ee68bce6c53801a3019b0fc1f1caa3ea761da821753a949724d3b1dca2457fd2b1df7c7f3879c4
dab41a20ab4ced8dd9e8b2ecf554fa412153dbcab52cc68ab4d83f7f310e0c5361f9c780160908816ff2e
f457db9aa93807da96de3068bfb63a18660d29d6efeb21b36c3c34abf83ff5847711eb85e052854498474
6965ceab0caae4fab0ae83bda024bf17d091132fdbf217f13d1c42e0671e324357c6d668492df202797f4
1a4a9be3d7598ee4d4530ca0fea76da94a225d93729eebee40f217a9d0a0dbdf28563a184eb1a71f8c6b0
0aa550fb21b0b1af62f98a5a165fb3e79d4265962e976c50875fbd374026e7fbe886eeee146d368899bad
54f97308f158ee3c33b290445497414186c47f3b54e78ed4fc8b5bf379b0169908cac2c654edb715f9b1a
3bc50992ffe9d4d5ba034b3a7128c50aaf2ec50497e68db2261b78f155900def3ece5d86b86f4a892a846
483ace0e008728627219bb71d897c726e9a90259c6fc61e4612ae76e41aa302e3193a0cf5d68d380fc7b0
7d41a757a459fc81fabc6336d21206b58f3ff06e390475f4e2b99ca3f0e4c82bb2d353375076d987d0a46
54aec2438a4c1dc17bd2dfc45a680fcb3b5144d860424b8890b83be8dba8c30ecb06cddd416e01d1917d2
eded83012bc19ae856dae5a6713895338a1f10c76260d61d25cc640292cbbe80897913e69c39a04d7c6b5
5e9b54dd661bf4f2fc9900283a6c668f82b8e25d0c750fa2fd00de1355e655b8e690d3d2dd1118d6199b1
a2723bc402fb38549bf13cacb217f42ab057fb2610d0f7306765d2c3644ee9384b1a8c0ccf847fdec7386
efb25ba2e3ad6a1b489aed02cd8a28be43855e4bb718e7647e299c150173e53855a199fef2a797d2d5e0c
454494cc175cdb205117614d1aebe6f402e21eed9dff22cfbcab47ededf6ae22717e83f0b4904c4051df6
03fd2ce44bf59f0ca07c065d08113bdf87b6c19891e07832d7d93a6845ddbd15d41cd416dddc8de81dbba
ade29c6f48c093c8df3c64aa69f8b1a36b79bc41cde01ab1758878b6dbb6b30c4d3cc5826bcf8ee3d159d
20289bf01ddca53c7978e8ca1180924fe3274cf855e2861645b24c527ea3f928e428a578c6cb791c8dc2a
96862aff4f0b383cfeaf325748f99510bbbc17158f038103157e293951db33b0307791b45e3750b781678
3e8a1eb9d2cffbb619bba9b40d55b3e19643acc3486d8c85e75c536033db333d83be39d5cffc02e1c48c7
ed56158365a50e9497474bedf48621f8c1ecb58bb87d99127e7d3b44d9ffdf49a967378b8e4a796f9ba1f
62d93433afa53443dcb145a27d2bc0d92b99be04f4142a1c94d497ff9477218caa0b318a04d676447a853
a51e725419f58374ed6823cd69ef7421d81009d2151fb4799781da7893177d46e9e39a3d2e5b7a2ef1ee4
585a606700a2e387dd4e261ce7840f817f5e80af8852689085ce27157ee2cb5398a78feffff635ab26350
11d739455c3fefdf16bd7b1d665a7daeb33019bbc7b4688786e58118f77a41e3879b68124d04a8de72479
428d222890cf07608fe56f9ad094c20d668d56d985083cd0c23a85da57e37095afb06c60c2c3664a13747
8f03438be98b78baa9af5e4d7fcde06b83952a59f4581ac51471fbc4203032f1fa52de74d804f24d99e3b
1ebd7177795f81a996225dbdfaedbaf007f6e92fd1e05f59c8864b55614b3d0a1adddc03198f7310ace88
254f71e115b8982d1701f6c4818a35f7c13523b81e2996fdd912c0160abbc2ef5b70c8e0bc5c3588b7269
e5152afaeb2cf84d106e2e8b1247754789e5714c600fa3df3502374c53e5bd6bd2bfe4533a3d0bc1ae7a4
368e811c1cc1047a0a8c085b2852e365735140404ca72c0e689848c3c4409037924118c59e7791f804152
00ea282df22aa541e28d271a27b2e50de4485675bb3c8461ff105a17daea67f2b699a42db0298d44d57ae
1dab3294399694f30fd2bdc30fb76637381e941c0f07736638cf8e532076160cd6c2a3810abd6d8ebbac4
7491021d878b593b854e41a9786e0dec869a7b038649becb63ee65ba9e20e309020068bb54269c442c542
5c0cb1d94785e2e1d98f142320e314010794ad009735fe274cb87e160d55baa8ff9ab8e0fc09f07953fec
afb1191fdd9b80d0c493baf72c4797feb7b5349c762d00d48d6c5322c7e58bd34d69fbf47ef9d8f1374c8
01198b8c59b97baf58c68a42581f9ff0a98cfd587f2707457e0a2df29616a750fe6877dc35d4e9066a67a
9d4b89560bd9fcfd3a896fc8e2b9d944efc4043d0301bdd7ce597c62da276a348adb4c837e925aa95318e
c20e305a194511f5cfb91076ac244dd4ee09179584241828134bbba779d16f09b8e54413462ae3a6aab5e
ca1340ae5314abe946e1674ad4f3d56b677c226727ca8009229441c5ac10cfeb8ce580629393178d42da0
7db214ac6596408353ada7b21f9e0d5d2388308042132d5cfac7940237d2acf9d4b873e0cf804c75412d7
fb5736e2cf6461d40009ecdb76ed0ee23d59e08d2be29e5229888a3d102faa676ccfd2cf44ad1dafd7101
98087fce312ccf89aaf93d6dbe1f32ee5f745d04018d0ba792281972b35ae99cf9ec3974a3ee233985cb9
a065d8219b285f181de26a1f154c73871d9164fc068cf86b97ceedbc0f4ef534efa2ab1e8df7cd850173b
24b8e6b3b5e683cbc3f50e79a674e89d51ff0a82a15e0e9952fc5d9468c2301f2fb4f3245692eddf6c690
6100640ab1d31acad8d834e55fdbcd7c82ab4334466ce761ee775fddb128a8308773346b73d7e472641b2
c7335855d6548d3a1edba40eb98a982694b503bc43fa61c91db1f2e18fce5cf8068be156c31b66554137d
cab75b034f18d4933acd5ec95d6d97146d327eadc8afaf00c3917418e421e4151c18d771bd79a7d8b860a
1fa9315c8bd847306b07e307c69faeeb0679c12cf4761ee21d809c58c2fa3b729904bc6175f755bce0930
ee2203591ff57e87b1ca577c1d7d75b5bf7f8d3215fd57af0f3d35a00c76f702c716ca2b9694ef185ee9d
2440cd28e2aa8e2e221c475c866699aa1ed7cc5c2c5e0d98bebab8bfd62aa33002c8ca3a58af1c3668c0b
fefcdea7388b9227d3155a06cf94b27ff93b5cf86331915c6c132fe1c092000b5e5f17d36193613ee70f1
8f672ab6543a65ab653cd47d13fcc138ae485e41710bb96903a7902a40fd1270697eff8e304bdc5c4797e
46c8837b7f644ec9acb11e146706f3a1254928373dc7df81d973dcc6d6b0b0443527a34bc31f9b1af586f
a667107ab5577c881aaae1b4725d02233a335be4d419c892a31eb397b9965f59f1532853bf456ad132a40
b3ea9d20b079ae07727f18918e5534b528ac5bc18f36a0880b7e29e0eac96456fd09e714ea63a8f79554d
9d38fe7033a143c01974e23d44e7e763f8dc193c018572afd4303b40af2bc2a91e6353264b6bd95e8f0a9
f683eb1e6e9d1ccabceabe9ff569b4d1d658d81c268a6837ed27b675d1adb1f79878828769778bb92649e
a29010509ec07d9d8403a21acdbc0f6032645f02908314537b15c7814092f783adea56561b6de27f7a7e4
a50f6014d6b3a7a4b56aef01a7fd3f90d829c77493b3505132a3afd275bb8d8debd2758cc3b574a78db81
b5ab1794192090ba341ae33a905fc138e4bb189275babe75a9ac1c94a477a65f70811e62f904cdbaaec9d
d8d200571d98308986b748974d9dedfaecad9c6dcfb514aadb1a0dadc351ef2b752ea6e8f31859aff8531
9be89de9b76107c4d1fe93e9063e9864559f477498922b1271fb4792c594c942dc7fe8de2c2423804cdb0
985dfdc7a68ff2eaf3323e38d5ce269d790cc7fcbe124025e7613e80dbd8edd3cf7ca106bd8650e1531eb
2fccac7b1fa5e66f7a94ccca1ed903b1d87500be464280c326167689fd4e99eaa25fd10904afdb9888e94
bf505483e26eb3fcaae078d9b4d8b47f0104cb572e12fd4854bd908939a6b714b1ef983f38de0408acddb
f560cc1beaf92b1c54f278b13d256011a915ea5ac7085134dd08d9b37ad08e6330891e0010b5809022b13
9394127b90a25c0cb5e521cef81c9650d5e976c88dfce8bfc6024f28e8ec0b8a0dd1b6036994e89c5506e
75af1a43b033bd55f38f6e37830da7ffc265ae85566927a993c7ac49f7e31a5a2795f198757a6f850d76c
2d4770336a73f05709603f660ff24e938454ec9f32b7fd873ab645cab0a82f1b865f5e277723fbe1adeab
c17784be0fc90fe7d44fdc6aa5938a6da20045cec6acdca7a15d301ab52f289c6172c1ce4bd19a5d94886
2413d2bd975534bc56dfecd733065d7db5df03a6dd807785b95c4acc763a2b570e1983633a446a3740e4a
a30e0e065d120560532f673b18f5bb33f9ca949a90850da679bf192c76b72b8a684cbbd17fe6740ef28d9
9788c69391e5489dc52f950e6f2d3df79e835d84fa0bcb8d4e0015f4b7e8fc6889db37d2438f9e91c8539
1d5785920ae05aeb391dd4a8875326b4b20aad9be2dc5b2127e3e5ab46158140026ed1ecef9ed9d2b1668
60d0df8e0b59082f64318c075d08bb5d6d03170261510f8f8996ec8195a4ee7a017c8060da2072673fb62
4f49fc542e5c605966a5eaa3cb26ad91721b101a21455c7b34823472cb11d05df5a767daf753e333c6141
bce8d5d166cc6aa9b52c298ce0464cbda39d5983bdc3b57bdbb01215e225e275e03914cb1262d07a5086b
9ac24b337eae21b1277c6a4937a94c21c44759cb2d8ac5f8cac59caa25d103245c4b462bfe955c927f235
1b086bc557baaf187a3fff06999a337b2a45d1cda8002feb0defe27e463050ba93a8474f4540fc22034ef
311a054fbe15f03643de443575808244134d5e9dbf7bd6cd939d592453ab3b7accf42cc797a276e63c581
63ab521bd1bdad3566bd1b1e10248cf7eeb5757c1f7c8ca9f976f4721b3ff780e7edfe2f37f20116fa090
5deb4fef0e5c5f2a303a865e6a0a6090afe237ba4b2c1437b569ec457d48c60dd5d878a93aafe3b3c626a
5368fedc33f32696fc88ca4a43b3646aad27a6241bdb5b1c273e57ddebaaa88449c54e63a1c8bc386c918
3d7b71bb95b0629e8a8f86973726f16b266c6393e3192f812554e73574679cbf3a67b3bbf969e00c904c9
89eb9c9fb19f3608810c72eb528253ac8606b1730b5ce4c3928a763da1399ea3ab531d3174a0a221f95de
ebc087b3b230734341b85c618f09865ab7c1dd66c74effa2b573de24b14f1385525873e15ab9d90f0c33d
fdcfa19de497675f5a3d9956bc2d66942325017e4132176922f08b478907f0a9e45ec64b23353db1d44e8
bb7f4060251afeb9e80dceab454eae609a3f5def899a2a42e4e7b62e7d6ae0735072d268bf7de73573070
c03546f57214a1e4ea1035bacba81c14147db07e0675ef87b88c14dd64f23c7e9b45d4dc68ac48e294221
af0b0d7b747373b03b7b922620e91ca810a13de10b02d13e139f68204d7ce0a2f8db69335b22b15e0bda4
9545435cc769e30273ee40d6d54a45256186ff348a52c0c82c8829fbf79d4e3edcc3f42c08b026b98dba9
e985d7597e085a767c3234182a0be06cd0435e40a5af588993f82c34e7651ea17ebee8f7035f29a378964
0913d812130e76460ec368c9a9a9607e0ecb66866311044b7f950dac488cd4479baa9a0b728f4c2925f04
e7bba448e8913b71178026789b3bf48713f619159a8c4c8347d5ea75e795e66c6662a24c4cd1325ba3bec
b127848779badddd62fa895df040135b2983c6c529e2bc097bc4c6c144853940903cecd3e0c8695f14d65
08a88c135a332b8def181bb0665d76cb6905cc7b87b2ca298cedc035d716be906a18da568351d3631a46c
42beb6925cbec36e3877b42fe660c45983a26230654b1a00e464576ecc4e9e98e3183915bc0bec1d724b6
4a7de15520e7f82bec8355d38878b3b2f80b731af2029a0f38c310c75a69b53af4f856c46f9772f028356
9dfb581e2caf1595414f3f0d74aa609483c1b
''')


def with_hdr(id, buf):
    return pack('<HH', id, len(buf)) + buf

client_private = gen_private_key(P256)
client_public = get_public_key(client_private, P256)

def make_cert():
    msg=(pack('<LL', 0x17, 0x20) +
            unhexlify('%064x' % client_public.x)[::-1] +
            (b'\0'*0x24) +
            unhexlify('%064x' % client_public.y)[::-1] +
            (b'\0'*0x4c))
    s=sign(msg, hs_key())
    s=DEREncoder().encode_signature(s[0], s[1])
    s=pack('<L', len(s)) + s
    msg = msg + s
    msg += b'\0'*(444 - len(msg))
    return msg

def encrypt_key():
    x = unhexlify('%064x' % client_public.x)[::-1]
    y = unhexlify('%064x' % client_public.y)[::-1]
    d = unhexlify('%064x' % client_private)[::-1]

    m = x+y+d
    iv = get_random_bytes(AES.block_size)
    aes = AES.new(psk_encryption_key, AES.MODE_CBC, iv)
    c = iv + aes.encrypt(m)
    sig = hmac.new(psk_validation_key, c, sha256).digest()
    return b'\x02' + c + sig
    

def make_flash_params(flash_size, sector_size, erase_cmd):
    return pack('<LLxxBx', flash_size, sector_size, erase_cmd)

cmd = unhex('4f 0000 0000')
# TODO lookup flash params from JEDEC ID returned by cmd 3f
#      currently, hardcoded for W25Q80B, 1MB, 4K sectors, 0x20 sector erase
cmd += with_hdr(0, make_flash_params(0x100000, 0x1000, 0x20)) 
cmd += with_hdr(1, b''.join([i + b'\0'*4 + sha256(i).digest() for i in flash_layout_hardcoded]))
cmd += with_hdr(5, make_cert())
cmd += with_hdr(3, crt_hardcoded)

usb=Usb()
usb.trace_enabled=True

tls=Tls(usb)
tls.trace_enabled=True
tls.handle_priv(encrypt_key())

db=Db(tls)

usb.open()
usb.cmd(enable_blob)
rsp=usb.cmd(unhex('3e'))
# ^ response contains flash_layout_hardcoded table sent via 4f previosly (if any). i.e.
# Given IC: W25Q80B, 1MB flash
#    flash JEDEC ID=ef:40, blks=0x1000, blksz=0x100 (0x100000 bytes)
# before 4f:
#    0000 ef00 4000 0010 1000 0001  0100 0000
# after 4f:
#    sts  id0  id1  blks ???  blksz      partitions
#    0000 ef00 4000 0010 0100 0001  0100 0500 
#           01 04 0700 00100000 00100000 
#           02 01 0200 00200000 00e00300
#           05 05 0300 00000400 00800000
#           06 06 0300 00800400 00800000
#           04 03 0500 00000500 00000300 
rsp=usb.cmd(cmd)
assert_status(rsp)
rsp=rsp[2:]
crt_len, rsp=rsp[:4], rsp[4:]
crt_len, = unpack('<L', crt_len)
tls.handle_cert(rsp[:crt_len])
# ^ TODO - validate cert
rsp = rsp[crt_len:]
# ^ TODO - figure out what the rest of rsp means

rsp=usb.cmd(unhex('01'))
assert_status(rsp)
# ^ get device info, contains firmware version which is needed to lookup pubkey for server cert validation

rsp=usb.cmd(unhex('50'))
# ^ TODO validate response
# It should be signed by the firmware private key. 
# The corresponding pub key is hardcoded for each fw revision in the synaWudfBioUsb.dll.
# for my device it is: x=f727653b4e16ce0665a6894d7f3a30d7d0a0be310d1292a743671fdf69f6a8d3, y=a85538f8b6bec50d6eef8bd5f4d07a886243c58b2393948df761a84721a6ca94
assert_status(rsp)
rsp=rsp[2:]
l,=unpack('<L', rsp[:4])
tls.handle_ecdh(rsp[l-400:])

rsp=usb.cmd(unhex('1a'))
assert_status(rsp)

tls.open()

# Wipe newly created partitions clean
db.erase_flash(1)
db.erase_flash(2)
db.erase_flash(5)
db.erase_flash(6)
db.erase_flash(4)

# Persist certs and keys on cert partition.
db.write_flash(1, 0, tls.makeTlsFlash())

# Reboot
tls.cmd(unhex('050200'))
