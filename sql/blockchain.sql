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

 Date: 06/04/2024 21:26:50
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
INSERT INTO `admininfo` VALUES ('AdminT 1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'b3h42lkh4j23hkl4j23hk4jh2kl3h4kjlh4k3jh5lk2j34h5l3k4jh5kl23jh', NULL, 1);
INSERT INTO `admininfo` VALUES ('AdminT 2', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'b3h42lkh4j23hkl4j23hk4jh2kl3h4kjlh4k3jh5lk2j34h5l3k4jh5kl23jh', NULL, 1);
INSERT INTO `admininfo` VALUES ('Test 1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'b3h42lkh4j23hkl4j23hk4jh2kl3h4kjlh4k3jh5lk2j34h5l3k4jh5kl23jh', NULL, 1);

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
INSERT INTO `pkadress` VALUES ('0cf1aa39a65f40092efdc1a5b86fc52cf09cbcd3b7ddbcdc2fe9572862aac33794d6c22d3f971f9fa6310e8ebb5641190a3521688db314a6ffba6f96012c7887', '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 3, 0, 'Machuchu');
INSERT INTO `pkadress` VALUES ('267e50ec5dfa53637f8c011014d4af61fcfe3fcd3d5efacbdcd58b9d7aadeb2e2f6b2d7075717941949ab461c9b54b55a1aaa33fe9767d5a5bb527735e491c7f', '18kKJjcGRKgnoX79ZWgiLNQWi25YvmMK2Q', 0, 0, 'Machuhan');
INSERT INTO `pkadress` VALUES ('73455b56ca624409cabff1753b1f7fa34a9f08b0a67cd2eaac85b71eada51694f9974c3478dca110cf5feb4d0d95196b0dac7b3bb28ff3a6f13ea46245bfe4a7', '1QKbYrLCHhQ8S1WYmUzgSonRvUZW5YDPZy', 0, 0, 'Machuchu');
INSERT INTO `pkadress` VALUES ('b8745f971b90629d68478c9cecc554f213bcce37780e6653a0ad41c39c3bbc6d64da7a0fac15d84e55d14962d77b39b29379c2fca6c5399c1131c7bd3211686a', '1CpR7UbMp93Ai3HhPZwSaoAhBjhtQVmyWQ', 0, 0, 'Machuchu');

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
INSERT INTO `proof_table` VALUES (1, 'picture', 'Machuhan');

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
INSERT INTO `transaction` VALUES ('79985cfc2359c089ab05044a4fa575f76b68a80a45371a3fbba4540736875099929b412f1bb28ce1255542f268b4a8f8cb06b168a368b86057da762b438af239', '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 0, 0, '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 'yes', '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 3);
INSERT INTO `transaction` VALUES ('system', 'system', 9.9, 0.1, '1HWupzTthp88LakvFmiPuJK2KJqCfrdDGn', 'not', NULL, 0);

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
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('Tset 1', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'qwer1234asdf5678zxcv9876qwer5678asdf1234zxcv7890qwer5678asdf1234', 'picture', 'not');
INSERT INTO `userinfo` VALUES ('Userk', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'picture', 'not');
INSERT INTO `userinfo` VALUES ('UserMark', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'qwer1234asdf5678zxcv9876qwer5678asdf1234zxcv7890qwer5678asdf1234', 'picture', 'yes');
INSERT INTO `userinfo` VALUES ('Usewrk', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'asjhw3472hjksd9871aflkjsd89231lasdajsdasjkdhasd789g2klh1kj3h4', 'picture', 'not');

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
INSERT INTO `volunteerinfo` VALUES ('Chu', '267053d88d4dfb2b7c5f69b8cc4b3d2ffa93cf897dd71c9b8bcf0af196450555');
INSERT INTO `volunteerinfo` VALUES ('Machuchu', 'da6472e753ad598060ee0a60d6f2feeda95defea4bf96b8a97ded6dd3a05f2fd');
INSERT INTO `volunteerinfo` VALUES ('Machuhan', 'da6472e753ad598060ee0a60d6f2feeda95defea4bf96b8a97ded6dd3a05f2fd');

SET FOREIGN_KEY_CHECKS = 1;
