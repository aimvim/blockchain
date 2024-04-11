/*
 Navicat Premium Data Transfer

 Source Server         : 123
 Source Server Type    : MySQL
 Source Server Version : 80036 (8.0.36)
 Source Host           : localhost:3306
 Source Schema         : blockchain

 Target Server Type    : MySQL
 Target Server Version : 80036 (8.0.36)
 File Encoding         : 65001

 Date: 08/04/2024 21:33:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admininfo
-- ----------------------------
DROP TABLE IF EXISTS `admininfo`;
CREATE TABLE `admininfo`  (
  `id` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` char(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `register_code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `invite_code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `status` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `admininfo_chk_1` CHECK (`status` in (0,1))
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admininfo
-- ----------------------------
INSERT INTO `admininfo` VALUES ('ADM0001', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'system', 'INVITE1234567890ABCD', 0);
INSERT INTO `admininfo` VALUES ('ADM0003', 'b6d767d2f8ed5d21a44b0e5886680cb9b7d033eb2ea29a6856b6a6e6e2e42e68', 'system', 'INVITE0987ZYXW6543VUTS', 0);
INSERT INTO `admininfo` VALUES ('ADM0005', '9e107d9d372bb6826bd81d3542a419d6e804eeb409d985256b6f8e4e44c28bdc', 'system', 'INVITEA1B2C3D4E5F6G7H8', 0);

-- ----------------------------
-- Table structure for mission_published
-- ----------------------------
DROP TABLE IF EXISTS `mission_published`;
CREATE TABLE `mission_published`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `area` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `begintime` datetime NULL DEFAULT NULL,
  `endtime` datetime NULL DEFAULT NULL,
  `activitytime` float NOT NULL,
  `award` double NOT NULL,
  `mcharacter` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `details` varchar(1000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `status` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'not finished',
  `checked` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'not',
  `uploader` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `uploader_company` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `volunteer` varchar(10000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `mission_published_chk_1` CHECK (`mcharacter` in (_utf8mb4'ABCD',_utf8mb4'EFGH',_utf8mb4'IJKL',_utf8mb4'MNOP')),
  CONSTRAINT `mission_published_chk_2` CHECK (`status` in (_utf8mb4'not finished',_utf8mb4'finished')),
  CONSTRAINT `mission_published_chk_3` CHECK (`checked` in (_utf8mb4'not',_utf8mb4'yes'))
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mission_published
-- ----------------------------
INSERT INTO `mission_published` VALUES (1, '敬老院活动', '敬老院', '2022-01-01 00:00:00', '2022-06-01 00:00:00', 3.5, 10, 'ABCD', '要好好打扫哦', 'finished', 'yes', 'Usermark', 'Global Solutions Inc.', 'Machuchu?Machuhan?');
INSERT INTO `mission_published` VALUES (2, '给老人买水果', '水果店', '2022-01-01 00:00:00', '2022-06-01 00:00:00', 0.5, 2, 'ABCD', '要挑好的水果买哦', 'not finished', 'yes', 'Usermark', 'Global Solutions Inc.', 'Machuhan?');
INSERT INTO `mission_published` VALUES (3, '探望老人', '老人的家', '2022-01-01 00:00:00', '2022-06-01 00:00:00', 2.5, 5, 'ABCD', '要好好照顾老人哦', 'not finished', 'not', 'Usermark', 'Global Solutions Inc.', NULL);

-- ----------------------------
-- Table structure for pkadress
-- ----------------------------
DROP TABLE IF EXISTS `pkadress`;
CREATE TABLE `pkadress`  (
  `pk` varchar(150) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `adress` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `tx_nonce` int NOT NULL DEFAULT 0,
  `amount` double NULL DEFAULT 0,
  `id` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`pk`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pkadress
-- ----------------------------
INSERT INTO `pkadress` VALUES ('00b0077c763967433b7e0cc2c0771dd6a55e75eb3d1ec8a484d0b6f85fb3ce9129ed3e44c89ebf3ebf343b98bcf661d1de9eb44c36e79e1027023fccc77e00fe', '16Cv8hNXDiPw4RSgUQmQhgomEdpTkMGe3Z', 0, 100, 'u1');
INSERT INTO `pkadress` VALUES ('05586722d89f73c9d91ba158f6bd7f258905af189510bd763ba4d6b368fee7c9c0e43d66c0d09a6312ac0216bb4cb6744c395ede96b0a9076557ac062999a2e1', '13qnyd1qbALaAsk3z1yDnqGEqnd3aa3wt2', 0, 100, 'u6');
INSERT INTO `pkadress` VALUES ('0a763e22b80c808fae453120d6107c43d5b155c673ea5b82761edae09e38c843941539334037942d547ed23d36f66f15696ed902575be320c2a3051c3d5ce3be', '1Dzuroyde27rtNfBrEDuNgRcGN7LKLGPA5', 0, 100, 'u5');
INSERT INTO `pkadress` VALUES ('0d0d4766786a48c139071b684bb1c36158deb225807543a2f9dba1fd9fc3d39c7015522dc6703f7acbc78d4e798f58bd65b07bcb0270cd4a1448b2b50e9cbf05', '1QHXZo4eANH23x4RJJYaMycwk8n2YjarWQ', 0, 100, 'u7');
INSERT INTO `pkadress` VALUES ('2ed047e3c1c00fba21548c44872386d4b943a428e5f1254241e4790fd9762adc5c75f5bb4476be420de09077ac50ef122b1d3dd5ad34f55b1a2f3472ee972679', '1AE4P95XofXcdMJDmKDuvxd9Jzk6auT7LB', 0, 100, 'u3');
INSERT INTO `pkadress` VALUES ('37c2c3f0926a3f1db3476644db15accb50847b7958fd48d4dad0697c6ed1d4b45d88f16083d77d236da6d6e8ecb5c97cf9604de1aba185d22eebcf740316ff96', '18CuZpdxhkawPzrtkknfKUzgf9CxFJzxSn', 0, 0, 'u2');
INSERT INTO `pkadress` VALUES ('485f36296fb242ed365ded3fc93a5c6d96fb42b7d56c9dedd77fde489f210eb1d92e67f096d4ef1b39c81f468666c4e14e505f8efdced7a7991131df886b39f3', '1AKF8kpYqZS9YMr68uoLG1mPTB23WQA5kn', 0, 100, 'u4');
INSERT INTO `pkadress` VALUES ('4ec00ac4f0ccbbe792fcaa37e06d327bfc493f5193b48565b9b58db72b32ea0d96cc72fd617ac4c76fa889012be4965ee9bc9029d699d7845e350633787337b4', '19ThMhDWDmrX8ro73M36b3bM2D5aNp53SA', 0, 0, 'u6');
INSERT INTO `pkadress` VALUES ('706e1ca2e8debe014c6a57b7cbe835837482dd0fa13ccb1f380994b6ad7b94a85008e70250dceb892b6c8d4b7002d945d964812dacbc3bff8cdbd1696fb48ccc', '18W7E3W6UpqWPtfRDdoAJw3hFhH2my99pU', 0, 0, 'u7');
INSERT INTO `pkadress` VALUES ('7d93f6fd2b2783aaf8e4defdce42be6730083338fe4c3a7ecb14511953a77916be8e4040f8a39e23de1d7dd6e8450f1766cf7e72732a916deada47698db07434', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 6, 0, 'u1');
INSERT INTO `pkadress` VALUES ('b2b7dfe5a025c7d2c9fe670a2ce39fe3c17640970472db53a8103ef83b1a299d869f51f05b8792be2e1e551f66a620dc28dceabf5d32683062cf1822f1511e9d', '1Lt2P4kYvgbrQagskfdsvme6PstLadvhRf', 0, 0, 'u8');
INSERT INTO `pkadress` VALUES ('bd70c3c6830de55d84abe51b6af421be811181fd1ede6b745cadf0de457fb2cc343be95a71153208c98eb3bbead1b1d4a8c807a8cf61029f8af7288c57f6fd06', '1774Fb3oMiwzubnbMXQ5AHYUBFYkXqGTds', 0, 0, 'u4');
INSERT INTO `pkadress` VALUES ('da41d1a277f0f3446458ec4647c309a0e145a907ad77bb09b6599962deaba2075035a0e6402a50ce7c7c275657463714c585df7c96db7ccbe53421e2cf6bd33c', '1EC7szbMNeuqbcA9BkcaUZSAn44cq2z9ZR', 0, 0, 'u5');
INSERT INTO `pkadress` VALUES ('ea4ae5295f55e26f7c32f09af1d91e49ad132df4b070e8b5fce4d69f89907732d02e3ef089928be53583a0e0703d9557bbd4c83e09f15cbe87bf59da120a719a', '1FqV6i3FBNf9sLgWjQabz2vobyK7Lkj8bw', 0, 0, 'u10');
INSERT INTO `pkadress` VALUES ('ed6754a09a939e049b64e2efc2195f2105bc9306d441eb1fec0cb426408a79ee7a9d58aaa9519f087ba14d47024604015eca2b4f55b8786947f9a8790fbb472a', '1BumoSppy3RpwRuEEUXgmdrq6ZQcqWs2Uq', 0, 0, 'u3');
INSERT INTO `pkadress` VALUES ('f64d527853dc4934156b98632afb84215dcf9702591725b88c98fe42f9ab18bdf81a409b90cf3b1a30227f3e8f4e30708fa996e03713c500fb4ee4ab8475e5db', '1PfJLZU8gCwpFobLET1MHWa1vWaerVoYs4', 0, 0, 'u9');
INSERT INTO `pkadress` VALUES ('ff76dcfaa9da36fff00589e6af2043feeeaafd0ac46a27de8dceec62ab97f2ec7136731f27e7d4b1d4f94e30efc2375a9299d5d0e226713bae0e56fb61d32af3', '1KexTucf78TYZFr6VkZ8M5Fc3yVZzfihNb', 0, 100, 'u2');

-- ----------------------------
-- Table structure for proof_table
-- ----------------------------
DROP TABLE IF EXISTS `proof_table`;
CREATE TABLE `proof_table`  (
  `id` int NULL DEFAULT NULL,
  `proof` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `uploader` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of proof_table
-- ----------------------------

-- ----------------------------
-- Table structure for register_code
-- ----------------------------
DROP TABLE IF EXISTS `register_code`;
CREATE TABLE `register_code`  (
  `code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `company` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of register_code
-- ----------------------------
INSERT INTO `register_code` VALUES ('asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'ACME Corporation');
INSERT INTO `register_code` VALUES ('b3h42lkh4j23hkl4j23hk4jh2kl3h4kjlh4k3jh5lk2j34h5l3k4jh5kl23jh', 'Widget Industries');
INSERT INTO `register_code` VALUES ('sldkfj23l4k23jh4lk23j4h2klj34h23l4kj2h34lkjh2lk34j23h4lkjh234l', 'Tech Innovations LLC');
INSERT INTO `register_code` VALUES ('qwer1234asdf5678zxcv9876qwer5678asdf1234zxcv7890qwer5678asdf1234', 'Global Solutions Inc.');
INSERT INTO `register_code` VALUES ('poiuytrewq0987zxcv7654qwer4321poiuytrewq1234asdf5678zxcv9876qwer', 'Main Street Bakery');

-- ----------------------------
-- Table structure for transaction
-- ----------------------------
DROP TABLE IF EXISTS `transaction`;
CREATE TABLE `transaction`  (
  `signature` char(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `senderadress` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `amount` double NULL DEFAULT NULL,
  `fees` double NULL DEFAULT NULL,
  `recipient` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `onchain` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT 'not',
  `miner` varchar(5102) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  `tx_nonce` int NOT NULL,
  CONSTRAINT `transaction_chk_1` CHECK (`onchain` in (_utf8mb3'yes',_utf8mb3'not'))
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of transaction
-- ----------------------------
INSERT INTO `transaction` VALUES ('851de40b2634ad196ca080c41c728ff1366e0c3a75592b9545e22b83dd8feb94557ce846e2ee25fdc7c3bdb49016e68702d4a303b25da411bc314cf35481ebe2', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '1BumoSppy3RpwRuEEUXgmdrq6ZQcqWs2Uq', 'not', NULL, 1);
INSERT INTO `transaction` VALUES ('f5595d9b67eab0ce33278f0cd5fb944bb5d5bc19fa2af0dfd474d7cfc0b15155dfbbabd29cc1d27d934d949ebaa7737b56aa20b8c1bce6b37f37ec75211157d4', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '1Lt2P4kYvgbrQagskfdsvme6PstLadvhRf', 'not', NULL, 2);
INSERT INTO `transaction` VALUES ('4582d68bef57e6f4d1f0028087dcb2eb2f92456a408003ac1edc16c27eefd8ff4a7a69cb9dcaa0c641ca9a32dd5bdfe95e197c6a13791f6d45cc46b36557d565', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '16Cv8hNXDiPw4RSgUQmQhgomEdpTkMGe3Z', 'not', NULL, 3);
INSERT INTO `transaction` VALUES ('2b8ab1beb0ff75c2f1eed255d7b63b4e5dc2e4d65683db70a71d7525f4112593304568e99a743013486b71ac1189850374645ec900848657f20f2ed74f4756c7', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '1Dzuroyde27rtNfBrEDuNgRcGN7LKLGPA5', 'not', NULL, 4);
INSERT INTO `transaction` VALUES ('3d2267973d36af7d8ff912d8565c4247c871faf9ce8e7ab07f771cee6ac6088967070cd15e09da8b6354575a2642b4212ca199ad64a6016581026828495af3e7', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '1AE4P95XofXcdMJDmKDuvxd9Jzk6auT7LB', 'not', NULL, 5);
INSERT INTO `transaction` VALUES ('f27f6ad4aa963cb4d0989f1f9fce44fc6097a2885c56287ec77d73cc2b915354934d9f5b5803539354799d8f27536d27afb1712c623d613eb26efbbefc8c5f4a', '1P15ZF8YotbDcquDHPVsGKEAXuXeqmZVbg', 0, 0, '1KexTucf78TYZFr6VkZ8M5Fc3yVZzfihNb', 'not', NULL, 6);

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo`  (
  `id` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` char(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `register_code` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `proof` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `checked` varchar(3) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `userinfo_chk_1` CHECK (`checked` in (_utf8mb4'yes',_utf8mb4'not'))
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('u1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u2', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u3', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u4', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u5', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u6', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');
INSERT INTO `userinfo` VALUES ('u7', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'jimod', 'yes');

-- ----------------------------
-- Table structure for volunteerinfo
-- ----------------------------
DROP TABLE IF EXISTS `volunteerinfo`;
CREATE TABLE `volunteerinfo`  (
  `id` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` char(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of volunteerinfo
-- ----------------------------
INSERT INTO `volunteerinfo` VALUES ('u1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u10', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u2', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u3', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u4', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u5', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u6', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u7', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u8', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');
INSERT INTO `volunteerinfo` VALUES ('u9', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225');

SET FOREIGN_KEY_CHECKS = 1;
