SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

SET AUTOCOMMIT = 0;

START TRANSACTION;

SET time_zone = "+00:00";

-- #############################################################
-- #############################################################
-- #############################################################




DROP TABLE IF EXISTS `admin`;

CREATE TABLE IF NOT EXISTS `admin` (
  
  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `nome` varchar(125) NOT NULL,
  
  `sobrenome` varchar(125) NOT NULL,
  
  `email` varchar(100) NOT NULL,
  
  `telefone` varchar(25) NOT NULL,
  
  `endereco` text NOT NULL,
  
  `senha` varchar(100) NOT NULL,
  
  `tipo` varchar(20) NOT NULL,
  
  `codigo_confirmacao` varchar(10) NOT NULL,
  
  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;


INSERT INTO `admin`
(`id`, `nome`, `sobrenome`, `email`, `telefone`, `endereco`, `senha`, `tipo`, `codigo_confirmacao`)
VALUES
(4, 'Nur', 'Mohsin', 'mohsin@gmail.com', '01677876551', 'Dhaka', '$5$rounds=535000$WOAOMdgoK2JpZLY5$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'manager', '0');


-- #############################################################
-- #############################################################
-- #############################################################



DROP TABLE IF EXISTS `pedidos`;

CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `usuario_id` int(11) DEFAULT NULL,
  
  -- !!!!!
  `ofname` text NOT NULL,
  
  `produto_id` int(11) NOT NULL,
  
  `quantidade` int(11) NOT NULL,
  
  `pedido_local` text NOT NULL,
  
  `telefone` varchar(15) NOT NULL,
  
  `entrega_status` varchar(10) NOT NULL DEFAULT 'no',
  
  `pedido_data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  `entrega_data` date DEFAULT NULL,
  
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;


INSERT INTO `pedidos` (`id`, `usuario_id`, `ofname`, `produto_id`, `quantidade`, `pedido_local`, `telefone`, `entrega_status`, `pedido_data`, `entrega_data`)
VALUES
(1, NULL, 'Kashmiri Chador', 1, 2, 'Khilkhet, Dhaka', '01609876543', 'no', '2018-09-21 13:05:07', NULL),
(2, NULL, 'Nur Mohsin', 1, 3, 'Khilkhet, Dhaka', '01609876543', 'no', '2018-09-21 13:08:55', NULL),
(3, NULL, 'Nur Mohsin', 2, 4, 'Dhaka', '09876543123', 'no', '2018-09-21 13:13:04', NULL),
(4, NULL, 'Nur Mohsin', 4, 1, 'Manikganj', '798345', 'no', '2018-09-21 13:18:47', NULL),
(5, NULL, 'Nur Mohsin', 9, 4, 'Dhaka, Bangladesh', '01609876543', 'no', '2018-09-22 02:01:02', NULL),
(6, NULL, 'Nur Mohsin', 2, 1, 'Manikganj', '01609876543', 'no', '2018-09-22 02:09:29', NULL),
(7, 9, 'Nur Mohsin', 2, 1, 'Manikganj', '01609876543', 'no', '2018-09-22 02:10:46', NULL),
(8, 9, 'Nur Mohsin', 1, 1, 'Manikganj', '0994', 'no', '2018-09-22 03:04:13', NULL),
(9, 9, 'Kashmiri Chador', 12, 4, 'Dhaka', '01609876543', 'no', '2018-09-22 03:21:14', '2018-09-29'),
(10, 9, 'Chador', 13, 1, 'Dhaka', '01609876543', 'no', '2018-09-22 03:22:05', '2018-09-29');



-- #############################################################
-- #############################################################
-- #############################################################





DROP TABLE IF EXISTS `produtos`;

CREATE TABLE IF NOT EXISTS `produtos` (

  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `produto_nome` varchar(100) NOT NULL,
  
  `preco` int(11) NOT NULL,
  
  `descricao` text NOT NULL,
  
  `disponivel` int(11) NOT NULL,
  
  `categoria` varchar(100) NOT NULL,
  
  `item` varchar(100) NOT NULL,
  
  `produto_codigo` varchar(20) NOT NULL,
  
  `foto` text NOT NULL,
  
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;


INSERT INTO `produtos`
(`id`, `produto_nome`, `preco`, `descricao`, `disponivel`, `categoria`, `item`, `produto_codigo`, `foto`, `data`)
VALUES
(1, 'T-Shirt', 120, 'T-Shirt', 4, 'camisa', 't-shirt', 't-007', 'MSTS14738.jpg', '2018-09-20 07:10:40'),
(2, 'Baborry wallet', 6000, 'Baborry-Double-Zipper-Coin-Bag-RFID-Blocking-Men-Wallets-New-Brand-PU-Leather-Wallet-Money-Purses', 3, 'carteira', 'carteira', 'w-004', 'IMG_1212.jpg', '2018-09-20 07:40:28'),
(3, 'Loafer Shoes', 2000, 'Loafer black shoes', 8, 'sapatos', 'sapatos', 's-001', '8544789_5_.jpg', '2018-09-20 08:33:57'),
(4, 'Artificial Belt', 1200, 'Black artificial belt', 9, 'cinto', 'cinto', 'b-001', '0283BLT.jpg', '2018-09-20 08:35:44'),
(5, 'Polo T-shirt', 500, 'Polo t-shirt', 10, 'camisa', 't-shirt', 's-002', 'lp00-2.jpg', '2018-09-20 08:40:06'),
(6, 'T-shirt', 300, 'Polo colorful t-shirt', 12, 'camisa', 't-shirt', 't-003', 'yellow_2_.jpg', '2018-09-20 08:41:18'),
(7, 'Tshirt', 200, 'Design t-shirt', 10, 'camisa', 't-shirt', 't-004', 'MSTSV14042.jpg', '2018-09-20 08:42:11'),
(8, 'T-shirt', 200, 'Color t-shirt', 20, 'camisa', 't-shirt', 't-005', 'MSTS14759.jpg', '2018-09-20 08:45:39'),
(9, 'Men\'s Tshirt', 500, 'Colorful men\'s t-shirt', 20, 'camisa', 't-shirt', 't-006', 'MSTSV14046.jpg', '2018-09-20 08:57:07'),
(10, 'Sports camisa', 1000, 'Real madrid t-shirt', 5, 'camisa', 't-shirt', 't-007', 'MSTSV14039.jpg', '2018-09-20 08:58:38'),
(12, 'T-shirt', 300, 'Design t-shirt', 10, 'camisa', 't-shirt', 't-010', 'MSTSV14049.jpg', '2018-09-20 09:02:04'),
(13, 'Leather Shoes', 2000, 'Best leather shoes', 10, 'sapatos', 'sapatos', 's-002', '8546789_5_.jpg', '2018-09-21 10:39:32'),
(14, 'cinto', 2000, 'Nice belt', 20, 'cinto', 'cinto', 'b-003', 'gbdl18_1.png', '2018-10-01 03:47:08'),
(15, 'cinto', 300, 'Nice one belt', 20, 'cinto', 'cinto', 'b-004', '101010_1_.jpg', '2018-10-01 03:48:09'),
(16, 'Mens Belt', 300, 'Mens belt', 15, 'cinto', 'cinto', 'b-005', 'image4_2.jpg', '2018-10-01 03:49:08'),
(17, 'Leather Wallet', 100, 'Leather wallet', 10, 'carteira', 'carteira', 'w-005', 'Baborry-Double-Zipper-Coin-Bag-RFID-Blocking-Men-Wallets-New-Brand-PU-Leather-Wallet-Money-Purses.jpg_640x640.jpg', '2018-10-01 03:51:52'),
(18, 'carteira', 300, 'carteira', 20, 'carteira', 'carteira', 'w-007', '1881_G.jpg', '2018-10-01 03:52:43'),
(19, 'Black walllet', 300, 'Black mens wallet', 20, 'carteira', 'carteira', 'w-009', 'image5_1_2.jpg', '2018-10-01 03:53:37'),
(20, 'Men\'s Shoes', 1200, 'Men\'s shoes', 23, 'sapatos', 'sapatos', 's-003', 'IMG_2429.jpg', '2018-10-01 03:56:41'),
(21, 'sapatos', 2000, 'Formal Shoes', 12, 'sapatos', 'sapatos', 's-004', 'G51A7054.jpg', '2018-10-01 03:57:24');



-- #############################################################
-- #############################################################
-- #############################################################




DROP TABLE IF EXISTS `produco_caracteristicas`;

CREATE TABLE IF NOT EXISTS `produto_caracteristicas` (

  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `produto_id` int(11) NOT NULL,
  
  `v_shape` varchar(10) NOT NULL DEFAULT 'no',
  
  `polo` varchar(10) NOT NULL DEFAULT 'no',
  
  `clean_text` varchar(10) NOT NULL DEFAULT 'no',
  
  `design` varchar(10) NOT NULL DEFAULT 'no',
  
  `chain` varchar(10) NOT NULL DEFAULT 'no',
  
  `leather` varchar(10) NOT NULL DEFAULT 'no',
  
  `hook` varchar(10) NOT NULL DEFAULT 'no',
  
  `color` varchar(10) NOT NULL DEFAULT 'no',
  
  `formal` varchar(10) NOT NULL DEFAULT 'no',
  
  `converse` varchar(10) NOT NULL DEFAULT 'no',
  
  `loafer` varchar(10) NOT NULL DEFAULT 'no',
  
  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;


INSERT INTO `produto_caracteristicas` (`id`, `produto_id`, `v_shape`, `polo`, `clean_text`, `design`, `chain`, `leather`, `hook`, `color`, `formal`, `converse`, `loafer`) VALUES
(1, 1, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(2, 2, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(3, 3, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(4, 4, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(5, 5, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(6, 6, 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(7, 7, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(9, 9, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(10, 10, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(14, 14, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no'),
(12, 12, 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(13, 13, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'),
(15, 15, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no'),
(16, 16, 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no'),
(17, 17, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(18, 18, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(19, 19, 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(20, 20, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'),
(21, 21, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no');



-- #############################################################
-- #############################################################
-- #############################################################




DROP TABLE IF EXISTS `produto_visita`;

CREATE TABLE IF NOT EXISTS `produto_visita` (

  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `usuario_id` int(11) NOT NULL,
  
  `produto_id` int(11) NOT NULL,
  
  `data` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;



INSERT INTO `produto_visita` (`id`, `usuario_id`, `produto_id`, `data`) VALUES
(1, 9, 9, '2018-09-22 02:19:30'),
(2, 9, 7, '2018-09-27 02:47:43'),
(3, 9, 12, '2018-09-22 03:20:59'),
(4, 9, 10, '2018-09-29 03:07:11'),
(5, 9, 5, '2018-09-22 03:19:19'),
(6, 9, 8, '2018-09-21 15:57:50'),
(7, 9, 6, '2018-09-22 02:12:54'),
(8, 9, 1, '2018-09-22 03:03:36');



-- #############################################################
-- #############################################################
-- #############################################################










DROP TABLE IF EXISTS `mensagens`;

CREATE TABLE IF NOT EXISTS `mensagens` (
  
    `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  
    `conteudo` varchar(255) NOT NULL,
  
    `autor_id` int(11) NOT NULL,
  
    `destinatario_id` int(11) NOT NULL,

    CONSTRAINT fk_autor_id FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON update cascade,
    
    CONSTRAINT fk_destinatario_id FOREIGN KEY (destinatario_id) REFERENCES usuarios(id) ON update cascade

) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;





DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE IF NOT EXISTS `usuarios` (

  `id` int(11) NOT NULL AUTO_INCREMENT,
  
  `nome` varchar(50) NOT NULL,
  
  `email` varchar(50) NOT NULL,
  
  `nome_usuario` varchar(25) NOT NULL,
  
  `senha` varchar(100) NOT NULL,
  
  `telefone` varchar(20) NOT NULL,
  
  `data_inscricao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  `online` varchar(1) NOT NULL DEFAULT '0',
  
  `ativo` varchar(3) NOT NULL DEFAULT 'sim',

  PRIMARY KEY (`id`)

) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;



INSERT INTO `usuarios` (`id`, `nome`, `email`, `nome_usuario`, `senha`, `telefone`, `data_inscricao`, `online`, `ativo`)
VALUES
(12, 'Mukul', 'mukul@gmail.com', 'mukul', '$5$rounds=535000$6PJhbzFlfJbcQbza$FbrPa3qqk1RJ5MSffRLO6LrQJXbgO8SudFuBpNf.wR7', '', '2018-07-23 14:09:14', '0', 'yes'),
(9, 'Nur Mohsin', 'mohsin@gmail.com', 'mohsin', '$5$rounds=535000$EnLkwqfGWGcWklRL$q9PbYw/TVXSzs.QpgUouZ3.6BzaPG2eLHkTyv.Qx80D', '123456789022', '2018-07-21 06:47:57', '1', 'yes'),
(14, 'Nur Mohsin', 'khan@gmail.com', 'khan', '$5$rounds=535000$wLKTQexvPQHueUsK$aFrFUXBHjrrAH61EFiYgj8cZECaaz8y6S5XS/zkkHw9', '', '2018-09-07 09:02:35', '0', 'yes'),
(13, 'Robin', 'robin@gmail.com', 'robin', '$5$rounds=535000$uiZc/VCwwa3XCTTe$Ec.JOjy4GkjpAXHtAvGt6pSc6KszajHgcyZy8v6Ivk1', '', '2018-07-26 12:36:57', '0', 'yes'),
(15, 'Sujon', 'sujon@yahoo.com', 'sujons', '$5$rounds=535000$aGykDT1yrocgTaDt$p2dDAMDz9g3N6o/Jj7QJY9B6NnMlUot.DCq/LOsCS13', '89345793753', '2018-09-08 13:58:36', '0', 'yes');
COMMIT;
