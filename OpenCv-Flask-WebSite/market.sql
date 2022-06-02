-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 17 May 2022, 13:27:44
-- Sunucu sürümü: 10.4.22-MariaDB
-- PHP Sürümü: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `market`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `product`
--

CREATE TABLE `product` (
  `pid` int(11) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(70) NOT NULL,
  `image` varchar(255) NOT NULL,
  `category` varchar(70) NOT NULL,
  `price` int(11) NOT NULL,
  `discount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `product`
--

INSERT INTO `product` (`pid`, `code`, `name`, `image`, `category`, `price`, `discount`) VALUES
(1, 'EDNALAN01', 'PORTAKAL', 'img_2.jpg', 'Meyve', 3, 100),
(2, 'EDNALAN02', 'LAYS', 'img_1.jpeg', 'Atıştırmalık', 5, 100),
(3, 'EDNALAN03', 'RUFFELS', 'img_3.jpeg', 'Atıştırmalık', 11, 50),
(4, 'EDNALAN04', 'COLA', 'img_4.jpeg', 'İçecek', 7, 150),
(5, 'EDNALAN05', 'ASPEROX', 'asperox.jpeg', 'Temizlik', 14, 75),
(6, 'EDNALAN06', 'KURU BADEM', 'badem.jpeg', 'Atıştırmalık', 22, 130),
(7, 'EDNALAN07', 'BİNGO', 'bingo.jpeg', 'Temizlik', 38, 100),
(8, 'EDNALAN08', 'EZOGELİN ÇORBA', 'corba.jpeg', 'Hazır Gıda', 7, 99),
(9, 'EDNALAN09', 'KREMALI BROKOLİ ÇORBASI', 'çorba.jpeg', 'Hazır Gıda', 6, 150),
(10, 'EDNALAN10', 'DAMAK BAKLAVA', 'damak.jpeg', 'Çikolata', 23, 50),
(11, 'EDNALAN11', 'SİGNAL DİŞ MACUNU', 'diş_macunu.jpeg', 'Temizlik', 24, 50),
(12, 'EDNALAN12', 'ÇİKOLATALI DONDURMA', 'dondurma.jpeg', 'Dondurma', 9, 50),
(13, 'EDNALAN13', 'ÇİLEK & ÇİKOLATA DODNURMA', 'dondurma2.jpeg', 'Dondurma', 9, 50),
(14, 'EDNALAN14', 'FAİRY BULAŞIK DETERJANI', 'fairy.jpeg', 'Temizlik', 38, 50);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `sepet`
--

CREATE TABLE `sepet` (
  `sepet_id` int(11) NOT NULL,
  `sepet_item` text DEFAULT NULL,
  `sepet_quantity` text DEFAULT NULL,
  `sepet_total_price` varchar(200) NOT NULL,
  `sepet_user_id` text DEFAULT NULL,
  `sepet_createdAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `sepet`
--

INSERT INTO `sepet` (`sepet_id`, `sepet_item`, `sepet_quantity`, `sepet_total_price`, `sepet_user_id`, `sepet_createdAt`) VALUES
(40, 'EDNALAN02', '10', '50', '{\'id\': 8}', '2022-05-16 20:45:16'),
(41, 'EDNALAN02', '1', '99', '{\'id\': 8}', '2022-05-16 20:45:57'),
(42, 'EDNALAN02', '1', '98', '{\'id\': 8}', '2022-05-17 08:39:09'),
(43, 'EDNALAN05', '1', '98', '{\'id\': 8}', '2022-05-17 08:40:35');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `sepettoplamlari`
--

CREATE TABLE `sepettoplamlari` (
  `sepetToplamlari_id` int(11) NOT NULL,
  `sepetToplamlari_sepetID` varchar(200) NOT NULL,
  `sepetToplamlari_toplam` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(3, 'Furkan Çetin', 'cetin@gmail.com', 'cetin', '123123'),
(8, 'cetin1', 'cetin1', 'cetin1', '1154'),
(9, 'Ahmet  Çetin', 'ahmet@gmail.com', 'ahmet', '123');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ürünler`
--

CREATE TABLE `ürünler` (
  `id` int(11) NOT NULL,
  `isim` text NOT NULL,
  `fiyat` int(11) NOT NULL,
  `kategori` text NOT NULL,
  `img` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `ürünler`
--

INSERT INTO `ürünler` (`id`, `isim`, `fiyat`, `kategori`, `img`) VALUES
(1, 'portakal', 6, 'Atıştırmalık', 'img_1.jpeg'),
(2, 'mandalina', 5, 'meyve', 'img_2.jpg'),
(3, 'kola', 7, 'İçecek', 'img_3.jpeg\r\n'),
(4, 'cips', 9, 'Atıştırmalık', 'img_4.jpeg'),
(5, 'Asperox', 16, 'Temizlik', 'asperox.jpeg');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`pid`);

--
-- Tablo için indeksler `sepet`
--
ALTER TABLE `sepet`
  ADD PRIMARY KEY (`sepet_id`);

--
-- Tablo için indeksler `sepettoplamlari`
--
ALTER TABLE `sepettoplamlari`
  ADD PRIMARY KEY (`sepetToplamlari_id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `ürünler`
--
ALTER TABLE `ürünler`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `product`
--
ALTER TABLE `product`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Tablo için AUTO_INCREMENT değeri `sepet`
--
ALTER TABLE `sepet`
  MODIFY `sepet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Tablo için AUTO_INCREMENT değeri `sepettoplamlari`
--
ALTER TABLE `sepettoplamlari`
  MODIFY `sepetToplamlari_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Tablo için AUTO_INCREMENT değeri `ürünler`
--
ALTER TABLE `ürünler`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
