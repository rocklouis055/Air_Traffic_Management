-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 24, 2023 at 09:39 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbms`
--

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `aid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  `avail` int(11) NOT NULL DEFAULT 3,
  `aname` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`aid`, `tid`, `type`, `avail`, `aname`) VALUES
(10, 1, 'International', 3, 'Blr'),
(10, 2, 'Domestic', 3, 'Blr'),
(20, 1, 'International', 3, 'Del'),
(20, 2, 'Domestic', 3, 'Del'),
(30, 1, 'International', 3, 'Hyd'),
(30, 2, 'Domestic', 3, 'Hyd'),
(72, 1, 'International', 10, 'Jpr'),
(72, 2, 'Domestic', 10, 'Jpr'),
(82, 1, 'International', 10, 'Goa'),
(82, 2, 'Domestic', 10, 'Goa');

-- --------------------------------------------------------

--
-- Table structure for table `avl`
--

CREATE TABLE `avl` (
  `aid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `date` date NOT NULL,
  `count` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `avl`
--

INSERT INTO `avl` (`aid`, `tid`, `date`, `count`) VALUES
(10, 1, '2022-12-10', 2),
(10, 1, '2023-01-24', 2),
(10, 1, '2023-01-31', 0),
(10, 2, '2023-01-23', 2),
(10, 2, '2023-01-26', 2),
(10, 2, '2023-01-30', 4),
(10, 2, '2023-01-31', 0),
(20, 1, '2022-12-30', 2),
(20, 1, '2023-01-23', 2),
(20, 2, '2022-12-10', 1),
(20, 2, '2023-01-26', 2),
(20, 2, '2023-02-02', 3),
(30, 1, '2022-12-10', 2),
(30, 1, '2023-01-26', 2),
(30, 1, '2023-01-30', 3),
(30, 1, '2023-01-31', 2),
(30, 1, '2023-02-02', 3),
(30, 1, '2023-02-15', 3),
(30, 2, '2023-01-26', 2),
(72, 1, '2022-12-10', 8),
(72, 1, '2022-12-30', 9),
(72, 1, '2023-01-24', 9),
(72, 1, '2023-01-31', 9),
(72, 1, '2023-02-15', 10);

-- --------------------------------------------------------

--
-- Stand-in structure for view `capassign`
-- (See below for the actual view)
--
CREATE TABLE `capassign` (
`capid` int(11)
,`count` bigint(21)
);

-- --------------------------------------------------------

--
-- Table structure for table `captain`
--

CREATE TABLE `captain` (
  `capid` int(11) NOT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `phno` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `captain`
--

INSERT INTO `captain` (`capid`, `fname`, `lname`, `gender`, `phno`) VALUES
(6002, 'sama', 'scotta', 'F', '1'),
(6003, 'janny', 'jonas', 'F', '456789123'),
(6004, 'chris', 'richard', 'M', '678912345'),
(6123, 'Jenna', 'Ortega', 'F', '1324567'),
(6850, 'Tom', 'Jerry', 'M', '987654321'),
(6855, 'Chris', 'Johnson', 'M', '456');

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `compid` int(11) NOT NULL,
  `compname` varchar(100) DEFAULT NULL,
  `compadd` varchar(100) DEFAULT NULL,
  `comptel` mediumtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`compid`, `compname`, `compadd`, `comptel`) VALUES
(3000, 'Indigo', 'Bangalore', '9876543210'),
(3001, 'GoAir', 'Delhi', '9976543210'),
(3002, 'SpiceJet', 'Chennai', '9886543210'),
(3003, 'AirIndia', 'Mumbai', '9877543210'),
(3004, 'AirAsia', 'Kolkata', '9876643210');

-- --------------------------------------------------------

--
-- Table structure for table `controlledby`
--

CREATE TABLE `controlledby` (
  `fid` int(11) NOT NULL,
  `capid1` int(11) NOT NULL,
  `capid2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `controlledby`
--

INSERT INTO `controlledby` (`fid`, `capid1`, `capid2`) VALUES
(109, 6855, 6004),
(110, 6004, 6850),
(151, 6003, 6002),
(187, 6855, 6850),
(193, 6002, 6003),
(195, 6003, 6002),
(199, 6004, 6850),
(1232, 6855, 6002),
(10011, 6003, 6004),
(12321, 6850, 6003),
(12322, 6123, 6004);

-- --------------------------------------------------------

--
-- Table structure for table `currenttable`
--

CREATE TABLE `currenttable` (
  `aid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `currentavail` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `currenttable`
--

INSERT INTO `currenttable` (`aid`, `tid`, `currentavail`) VALUES
(10, 1, 3),
(10, 2, 1),
(20, 1, 2),
(20, 2, 3),
(30, 1, 3),
(30, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `fid` int(11) NOT NULL,
  `fno` int(11) DEFAULT NULL,
  `fdate` date DEFAULT NULL,
  `ftime` int(11) DEFAULT NULL,
  `pasno` int(11) DEFAULT NULL,
  `flightdept` time DEFAULT NULL,
  `flightarrival` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`fid`, `fno`, `fdate`, `ftime`, `pasno`, `flightdept`, `flightarrival`) VALUES
(109, 567, '2023-01-26', 100, 100, '10:00:00', '11:40:00'),
(110, 2314, '2023-02-15', 100, 102, '10:10:10', '11:50:10'),
(151, 1322, '2023-01-31', 100, 100, '20:30:39', '22:10:39'),
(187, 12, '2023-01-31', 20, 21, '20:10:10', '20:30:10'),
(193, 1341, '2023-01-26', 100, 123, '10:10:10', '11:50:10'),
(195, 213, '2023-01-24', 500, 121, '10:10:10', '18:30:10'),
(199, 124, '2023-01-23', 100, 10, '20:20:20', '22:00:20'),
(1232, 1231, '2022-12-10', 60, 100, '10:00:00', '11:00:00'),
(10011, 12374, '2022-12-30', 180, 1000, '01:00:00', '04:00:00'),
(12321, 1231, '2022-12-10', 60, 100, '10:00:00', '11:00:00'),
(12322, 1231, '2022-12-10', 60, 100, '10:00:00', '11:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `fromto`
--

CREATE TABLE `fromto` (
  `fid` int(11) NOT NULL,
  `aid1` int(11) NOT NULL,
  `tid1` int(11) NOT NULL,
  `aid2` int(11) NOT NULL,
  `tid2` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fromto`
--

INSERT INTO `fromto` (`fid`, `aid1`, `tid1`, `aid2`, `tid2`) VALUES
(109, 20, 2, 30, 2),
(110, 30, 1, 72, 1),
(151, 10, 1, 10, 2),
(187, 10, 1, 10, 2),
(193, 10, 2, 30, 1),
(195, 10, 1, 72, 1),
(199, 10, 2, 20, 1),
(1232, 10, 1, 30, 1),
(10011, 20, 1, 72, 1),
(12321, 72, 1, 20, 2),
(12322, 72, 1, 20, 2);

--
-- Triggers `fromto`
--
DELIMITER $$
CREATE TRIGGER `trfromto` AFTER INSERT ON `fromto` FOR EACH ROW BEGIN
	DECLARE aid int;
    DECLARE tid int;
	DECLARE d date;
	DECLARE c int;
	DECLARE temp int;
	DECLARE aid11 int;
	DECLARE tid11 int;
	DECLARE c1 int;
	DECLARE temp1 int;
    
	set temp1=Null;
	set temp=Null;
    
	select fromto.aid2,fromto.tid2,flight.fdate,fromto.aid1,fromto.tid1
	into aid,tid,d,aid11,tid11
	from fromto,flight
	where flight.fid=fromto.fid and flight.fid=new.fid;
    
	select a.avail
	into c
	from airport a
	where a.aid=aid and a.tid=tid;
    
	select a.avail
	into c1
	from airport a
	where a.aid=aid11 and a.tid=tid11;
    
	select avl.count
	into temp
	from avl
	WHERE avl.aid=aid and avl.tid=tid and avl.date=d;
    
	select avl.count
	into temp1
	from avl
	WHERE avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
    
	if temp is Null THEN
		insert INTO avl values(aid,tid,d,c-1);
	else
		UPDATE avl set avl.count=avl.count-1 where avl.aid=aid and avl.tid=tid and avl.date=d;
	end if;
    
	if temp1 is Null THEN
		insert INTO avl values(aid11,tid11,d,c1-1);
	else
		UPDATE avl set avl.count=avl.count-1 where avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
	end if;
    
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trfromtodel` BEFORE DELETE ON `fromto` FOR EACH ROW BEGIN
    DECLARE aid int;
    DECLARE tid int;
    DECLARE d date;
    DECLARE c int;
    DECLARE temp int;
    DECLARE aid11 int;
    DECLARE tid11 int;
    DECLARE c1 int;
    DECLARE temp1 int;
    set temp1=NULL;
    set temp=NULL;
    
    select flight.fdate
    into d
    from fromto,flight
    where flight.fid=fromto.fid and flight.fid=old.fid;
    
    set aid=old.aid2;
    set tid=old.tid2;
    set aid11=old.aid1;
    set tid11=old.tid1;
    
    UPDATE avl set avl.count=avl.count+1 where avl.aid=aid and avl.tid=tid and avl.date=d;
    UPDATE avl set avl.count=avl.count+1 where avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
    INSERT INTO fokat VALUES(aid11,tid11,d,aid,tid);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trfromtoup` AFTER UPDATE ON `fromto` FOR EACH ROW BEGIN
    DECLARE aid int;
    DECLARE tid int;
    DECLARE d date;
    DECLARE c int;
    DECLARE temp int;
    DECLARE aid11 int;
    DECLARE tid11 int;
    DECLARE c1 int;
    DECLARE temp1 int;
    set temp1=NULL;
    set temp=NULL;
    
    select fromto.aid2,fromto.tid2,flight.fdate,fromto.aid1,fromto.tid1
    into aid,tid,d,aid11,tid11
    from fromto,flight
    where flight.fid=fromto.fid and flight.fid=new.fid;
    
    select a.avail
    into c
    from airport a
    where a.aid=aid and a.tid=tid;
    
    select a.avail
    into c1
    from airport a
    where a.aid=aid11 and a.tid=tid11;
    select avl.count
    into temp
    from avl
    WHERE avl.aid=aid and avl.tid=tid and avl.date=d;
    
    select avl.count
    into temp1
    from avl
    WHERE avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
    
    if temp is Null THEN
        insert INTO avl values(aid,tid,d,c-1);
    else
        UPDATE avl set avl.count=avl.count-1 where avl.aid=aid and avl.tid=tid and avl.date=d;
    end if;
    
    
    
    if temp1 is Null THEN
        insert INTO avl values(aid11,tid11,d,c1-1);
    else
        UPDATE avl set avl.count=avl.count-1 where avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
    end if;
    
    select flight.fdate
    into d
    from fromto,flight
    where flight.fid=fromto.fid and flight.fid=new.fid;
    
    set aid=old.aid2;
    set tid=old.tid2;
    set aid11=old.aid1;
    set tid11=old.tid1;
    
    UPDATE avl set avl.count=avl.count+1 where avl.aid=aid and avl.tid=tid and avl.date=d;
    UPDATE avl set avl.count=avl.count+1 where avl.aid=aid11 and avl.tid=tid11 and avl.date=d;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `latestflight`
-- (See below for the actual view)
--
CREATE TABLE `latestflight` (
`capid` int(11)
,`fdate` date
,`flightarrival` time
,`aid2` int(11)
,`tid2` int(11)
,`lastflight` time
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `notassignflight`
-- (See below for the actual view)
--
CREATE TABLE `notassignflight` (
`fid` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `plane`
--

CREATE TABLE `plane` (
  `pid` int(11) NOT NULL,
  `pno` int(11) DEFAULT NULL,
  `ptype` varchar(20) DEFAULT NULL,
  `pflydate` datetime DEFAULT NULL,
  `pflytime` int(11) DEFAULT NULL,
  `compid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plane`
--

INSERT INTO `plane` (`pid`, `pno`, `ptype`, `pflydate`, `pflytime`, `compid`) VALUES
(1000, 2000, 'boeing', NULL, 0, 3000),
(1001, 2001, 'boeing', '2022-12-30 00:00:00', 240, 3004),
(1002, 2002, 'boeing', '2022-12-10 00:00:00', 60, 3001),
(1003, 2003, 'boeing', '2022-12-10 00:00:00', 60, 3002),
(1004, 2004, 'boeing', NULL, 0, 3003);

-- --------------------------------------------------------

--
-- Table structure for table `takes`
--

CREATE TABLE `takes` (
  `pid` int(11) NOT NULL,
  `fid` int(11) NOT NULL,
  `flag` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `takes`
--

INSERT INTO `takes` (`pid`, `fid`, `flag`) VALUES
(1001, 109, 0),
(1001, 1232, 1),
(1001, 10011, 1),
(1002, 12321, 1),
(1003, 12322, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `role` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userid`, `name`, `password`, `role`) VALUES
(1, 'admin', 'admin', 'admin'),
(2, 'normal', 'normal', 'normal');

-- --------------------------------------------------------

--
-- Structure for view `capassign`
--
DROP TABLE IF EXISTS `capassign`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `capassign`  AS   (select `c`.`capid` AS `capid`,count(`b`.`fid`) AS `count` from (`captain` `c` left join `controlledby` `b` on(`c`.`capid` = `b`.`capid1` or `c`.`capid` = `b`.`capid2`)) group by `c`.`capid` order by count(`b`.`fid`))  ;

-- --------------------------------------------------------

--
-- Structure for view `latestflight`
--
DROP TABLE IF EXISTS `latestflight`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `latestflight`  AS   (select `c`.`capid` AS `capid`,`f`.`fdate` AS `fdate`,`f`.`flightarrival` AS `flightarrival`,`t`.`aid2` AS `aid2`,`t`.`tid2` AS `tid2`,max(`f`.`flightarrival`) AS `lastflight` from (((`captain` `c` join `controlledby` `b`) join `fromto` `t`) join `flight` `f`) where (`c`.`capid` = `b`.`capid1` or `c`.`capid` = `b`.`capid2`) and `b`.`fid` = `f`.`fid` and `f`.`fid` = `t`.`fid` group by `c`.`capid`,`f`.`fdate`)  ;

-- --------------------------------------------------------

--
-- Structure for view `notassignflight`
--
DROP TABLE IF EXISTS `notassignflight`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `notassignflight`  AS   (select `f`.`fid` AS `fid` from `flight` `f` where !(`f`.`fid` in (select `t`.`fid` from `controlledby` `t`)))  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`aid`,`tid`);

--
-- Indexes for table `avl`
--
ALTER TABLE `avl`
  ADD PRIMARY KEY (`aid`,`tid`,`date`);

--
-- Indexes for table `captain`
--
ALTER TABLE `captain`
  ADD PRIMARY KEY (`capid`);

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`compid`);

--
-- Indexes for table `controlledby`
--
ALTER TABLE `controlledby`
  ADD PRIMARY KEY (`fid`,`capid1`,`capid2`),
  ADD KEY `capid1` (`capid1`),
  ADD KEY `capid2` (`capid2`);

--
-- Indexes for table `currenttable`
--
ALTER TABLE `currenttable`
  ADD PRIMARY KEY (`aid`,`tid`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`fid`);

--
-- Indexes for table `fromto`
--
ALTER TABLE `fromto`
  ADD PRIMARY KEY (`fid`,`aid1`,`tid1`,`aid2`,`tid2`),
  ADD KEY `aid1` (`aid1`,`tid1`),
  ADD KEY `aid2` (`aid2`,`tid2`);

--
-- Indexes for table `plane`
--
ALTER TABLE `plane`
  ADD PRIMARY KEY (`pid`),
  ADD KEY `compid` (`compid`);

--
-- Indexes for table `takes`
--
ALTER TABLE `takes`
  ADD PRIMARY KEY (`pid`,`fid`),
  ADD KEY `fid` (`fid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `avl`
--
ALTER TABLE `avl`
  ADD CONSTRAINT `avl_ibfk_1` FOREIGN KEY (`aid`,`tid`) REFERENCES `airport` (`aid`, `tid`);

--
-- Constraints for table `controlledby`
--
ALTER TABLE `controlledby`
  ADD CONSTRAINT `controlledby_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `flight` (`fid`) ON DELETE CASCADE,
  ADD CONSTRAINT `controlledby_ibfk_2` FOREIGN KEY (`capid1`) REFERENCES `captain` (`capid`) ON DELETE CASCADE,
  ADD CONSTRAINT `controlledby_ibfk_3` FOREIGN KEY (`capid2`) REFERENCES `captain` (`capid`) ON DELETE CASCADE;

--
-- Constraints for table `currenttable`
--
ALTER TABLE `currenttable`
  ADD CONSTRAINT `currenttable_ibfk_1` FOREIGN KEY (`aid`,`tid`) REFERENCES `airport` (`aid`, `tid`);

--
-- Constraints for table `fromto`
--
ALTER TABLE `fromto`
  ADD CONSTRAINT `fromto_ibfk_1` FOREIGN KEY (`aid1`,`tid1`) REFERENCES `airport` (`aid`, `tid`) ON DELETE CASCADE,
  ADD CONSTRAINT `fromto_ibfk_2` FOREIGN KEY (`aid2`,`tid2`) REFERENCES `airport` (`aid`, `tid`) ON DELETE CASCADE,
  ADD CONSTRAINT `fromto_ibfk_3` FOREIGN KEY (`fid`) REFERENCES `flight` (`fid`) ON DELETE CASCADE;

--
-- Constraints for table `plane`
--
ALTER TABLE `plane`
  ADD CONSTRAINT `plane_ibfk_1` FOREIGN KEY (`compid`) REFERENCES `company` (`compid`) ON DELETE SET NULL;

--
-- Constraints for table `takes`
--
ALTER TABLE `takes`
  ADD CONSTRAINT `takes_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `plane` (`pid`),
  ADD CONSTRAINT `takes_ibfk_2` FOREIGN KEY (`fid`) REFERENCES `flight` (`fid`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
