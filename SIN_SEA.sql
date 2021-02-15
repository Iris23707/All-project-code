-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 14, 2020 at 12:29 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SIN_SEA`
--

-- --------------------------------------------------------

--
-- Table structure for table `Class`
--

CREATE TABLE `Class` (
  `Class_ID` varchar(30) NOT NULL,
  `Class_Name` varchar(50) NOT NULL,
  `Student_NO` int(255) NOT NULL DEFAULT '0',
  `Dept_ID` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Class`
--

INSERT INTO `Class` (`Class_ID`, `Class_Name`, `Student_NO`, `Dept_ID`) VALUES
('ACCT1', 'Accounting class1', 50, 1),
('ACCT2', 'Accounting class2', 35, 1),
('CHEM1', 'Chemical class1', 23, 2),
('DS1', 'Data Science class1', 35, 3),
('ECON1', 'Economics class1', 20, 1),
('HEAL1', 'Health class1', 52, 5),
('IT1', 'Information System class1', 68, 3),
('MED1', 'Medicine class1', 30, 4),
('PHAR1', 'Pharmacy class1', 25, 4),
('PHY1', 'Physics class1', 45, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Compulsory`
--

CREATE TABLE `Compulsory` (
  `Course_ID` varchar(50) NOT NULL,
  `Course_Name` varchar(50) NOT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Credit` decimal(4,2) DEFAULT NULL,
  `C_Drescription` varchar(1000) DEFAULT NULL,
  `Teacher_ID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Compulsory`
--

INSERT INTO `Compulsory` (`Course_ID`, `Course_Name`, `Department`, `Credit`, `C_Drescription`, `Teacher_ID`) VALUES
('ACCT7101', 'Accounting', 'Business', '2.00', 'An introductory course that equips students with an integrated base of theoretical and technical knowledge and skills in financial accounting. Financial accounting is a system used to prepare reports that disseminate information about the performance and financial status of a business to external parties.', 'T128'),
('CHEM3001', 'Advanced Organic Chemistry', 'Science', '2.00', 'Molecular conformations, effective sizes of groups. Types of organic transformations & their mechanisms: stereochemical outcomes, structural effects on reactivity, role of intermediates. Analytical approaches to organic synthesis: reagents, methodologies, specificities & stereochemistry, illustrated by synthesis of natural & non-natural compounds. Functional group & whole molecule retrosynthesis.', 'T224'),
('COMP7500', 'Advanced Algorithms & Data Structures', 'Engineering', '2.00', 'Analysis of algorithms. Solution of summation & recurrence equations. Algorithm paradigms: divide-&-conquer, greedy algorithms, dynamic programming, backtracking, branch-&-bound. Advanced graph algorithms. Amortised analysis. Self-adjusting data structures. Complexity classes, NP-completeness. Approximation algorithms. Randomized algorithms.', 'T386'),
('DATA7202', 'Statistical Methods for Data Science', 'Engineering', '2.00', 'This course will provide students with the core ideas which are important for analysing and interpreting massive data sets. These include modelling techniques: Linear models, smoothing regularisation and LASSO methods for big datasets and logistic regression.', 'T303'),
('ECON7310', 'Elements of Econometrics', 'Business', '2.00', 'Introductory applied econometric course for students with basic economic statistics background. Topics covered include: economic models and role of econometrics, linear regression, general linear model, hypothesis testing, specification testing, dummy variables, simple dynamic models and simple cointegration models. Tutorial problems are solved using a relevant econometrics program.', 'T152'),
('MEDI7285', 'Introduction to Digital Health', 'Medicine', '2.00', 'This course will examine the impact of ICT integration in healthcare along with other factors such as human resources, economics and government policies. This course will set students on the path to thinking critically about issues related to digital health.', 'T416'),
('MKTG7501', 'Fundamentals of Marketing', 'Business', '2.00', 'Introduction to marketing management; consumer behaviour; marketing research & segmentation; product life cycle theory; product & pricing strategies; distribution & logistics; promotional strategy including advertising & personal selling; marketing organisation, planning & control; international marketing, services marketing & marketing for not-for-profit organisations.', 'T136'),
('PHRM3042', 'Pharmaceutical Discovery & Microbiology', 'Medicine', '2.00', 'Pharmaceutical microbiology relating to the principles and practice of pharmacy. Drug design and structure activity relationships of drugs used for: i) the treatment or prophylaxis of infections, ii) the treatment or management of respiratory conditions, and iii) the treatment of cancers.', 'T460'),
('PHYS3071', 'Computational Physics', 'Science', '2.00', 'Computational physics involving the Unix/Linux operating system environment and C programming. This is an introduction to computer programming & relevant numerical & graphical methods as applied to a range of physics problems. Topics include classical dynamics (ODEs).', 'T239'),
('PUBH3005', 'Influencing Health Behaviours', 'Health', '2.00', 'This course provides an overview of an evidence-based approach to the development, implementation and evaluation of health behaviour interventions.', 'T511');

-- --------------------------------------------------------

--
-- Table structure for table `Department`
--

CREATE TABLE `Department` (
  `Dept_ID` int(30) NOT NULL,
  `Dept_Name` varchar(50) NOT NULL,
  `D_Mail` varchar(100) DEFAULT NULL,
  `Director` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Department`
--

INSERT INTO `Department` (`Dept_ID`, `Dept_Name`, `D_Mail`, `Director`) VALUES
(1, 'Business', 'bel@uq.edu.au', 'Professor Andrew Griffiths'),
(2, 'Science', 'enquire@science.uq.edu.au', 'Professor Melissa Brown'),
(3, 'Engineering', 'enquiries@eait.uq.edu.au', 'Professor Vicki Chen'),
(4, 'Medicine', 'med.enquiries@uq.edu.au', 'Professor Stuart Carney'),
(5, 'Health', 'habs@uq.edu.au', 'Professor Bruce Abernethy');

-- --------------------------------------------------------

--
-- Table structure for table `Enrollment`
--

CREATE TABLE `Enrollment` (
  `Grade` int(100) NOT NULL,
  `Student_ID` varchar(30) NOT NULL,
  `Course_ID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Enrollment`
--

INSERT INTO `Enrollment` (`Grade`, `Student_ID`, `Course_ID`) VALUES
(90, '123', 'ACCT7101'),
(83, '123', 'MKTG7501'),
(89, '123', 'ECON7310'),
(81, '236', 'ECON7310'),
(78, '236', 'ACCT7101'),
(82, '236', 'MKTG7501'),
(88, '354', 'MKTG7501'),
(76, '354', 'ACCT7101'),
(91, '354', 'ECON7310'),
(87, '369', 'COMP7500'),
(97, '369', 'DATA7202'),
(95, '701', 'DATA7202'),
(85, '701', 'COMP7500'),
(85, '459', 'PUBH3005'),
(80, '521', 'MEDI7285'),
(90, '521', 'PHRM3042'),
(90, '606', 'PHRM3042'),
(95, '606', 'MEDI7285'),
(95, '714', 'CHEM3001'),
(77, '842', 'CHEM3001'),
(87, '842', 'PHYS3071'),
(81, '714', 'PHYS3071');

-- --------------------------------------------------------

--
-- Table structure for table `Project`
--

CREATE TABLE `Project` (
  `Project_ID` varchar(50) NOT NULL,
  `Project_Name` varchar(50) NOT NULL,
  `Project_Level` varchar(50) DEFAULT NULL,
  `Teacher_ID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Project`
--

INSERT INTO `Project` (`Project_ID`, `Project_Name`, `Project_Level`, `Teacher_ID`) VALUES
('P11', 'Income inequality in Australia', 'QLD I', 'T128'),
('P12', 'The hotel of healing', 'QLD II', 'T136'),
('P13', 'A decade of serving the community', 'Brisbane II', 'T152'),
('P21', 'Energy, materials and light', 'UQ I', 'T224'),
('P22', 'Microbes and molecules', 'AU II', 'T239'),
('P31', 'Making Spatiotemporal Data More Useful', 'UQ I', 'T303'),
('P32', 'Microwave Inspection and Detection Systems', 'QLD III', 'T386'),
('P41', 'Inventing new clinical medicine', 'AU II', 'T416'),
('P42', 'Child Health Research', 'Brisbane III', 'T460'),
('P5', 'Health, well-being and ageing', 'AU I', 'T511');

-- --------------------------------------------------------

--
-- Table structure for table `Selective`
--

CREATE TABLE `Selective` (
  `Course_ID` varchar(50) NOT NULL,
  `Course_Name` varchar(50) NOT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Credit` decimal(4,2) DEFAULT NULL,
  `S_Drescription` varchar(1000) DEFAULT NULL,
  `Teacher_ID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Selective`
--

INSERT INTO `Selective` (`Course_ID`, `Course_Name`, `Department`, `Credit`, `S_Drescription`, `Teacher_ID`) VALUES
('ACCT3103', 'Advanced Financial Accounting', 'Business', '2.00', 'Accounting for corporate group structures, joint arrangements, associates, foreign currency translations, operating segments, external administration and capital structures.', 'T128'),
('ACCT3104', 'Management Accounting', 'Business', '2.00', 'Accounting information relevant for planning, control & performance evaluation decisions by management in business & non-business organisations; alternative analyses & systems; conceptual issues & behavioural implications.', 'T136'),
('COMP7702', 'Artificial Intelligence', 'Engineering', '2.00', 'Methods & techniques within the field of artificial intelligence, including problem solving and optimisation by search, representing and reasoning with uncertain knowledge and machine learning. Specific emphasis on the practical utility of algorithms and their implementation in software.', 'T386'),
('DATA7703', 'Machine Learning for Data Scientists', 'Engineering', '2.00', 'Machine learning is a branch of artificial intelligence concerned with the development & application of adaptive algorithms that use example data or previous experience to solve a given problem.', 'T303'),
('ECON7390', 'Financial Econometrics', 'Business', '2.00', 'This course gives an introduction to various aspects of financial econometrics. Characteristics of financial data will be studied and several major econometric models used in finance will be surveyed. Students learn how to analyse financial data and are introduced to some of the major tools used in both in the literature and by practitioners.', 'T152'),
('MEDI7284', 'Introduction to Rural and Remote Medicine', 'Medicine', '2.00', 'This course covers occupational health, safety and wellness in the rural context and how these impact on the health and well-being of people living in rural and remote communities.', 'T416'),
('NUTR2003', 'Nutrition in the Lifespan', 'Health', '2.00', 'This course provides an understanding of the significance of nutrition across the lifespan, using a public health perspective. This course reviews the nutritional and dietary requirements of humans for different periods of their lifespan and for specific physiological states. ', 'T511'),
('PHRM2021', 'Dosage Form Design A1', 'Medicine', '2.00', 'The study and application of physicochemical principles to the design, formulation and effective use of liquid and semi-solid dosage forms. The basic principles of biotechnology as they pertain to the pharmaceutical industry will be introduced.', 'T460'),
('PHYS1001', 'Mechanics & Thermal Physics I', 'Science', '2.00', 'Nature of physics, kinematics, dynamics, conservation laws, rigid body rotation, oscillations, fluids and elasticity, thermodynamics, arrow of time, heat engines, laboratory experiments & error analysis.', 'T239'),
('SCIE1000', 'Theory & Practice in Science', 'Science', '2.00', 'This foundation course in science introduces students to the broad range of mathematical, analytical, conceptual and computational tools employed by scientists to develop, analyse and interpret models of scientific processes.', 'T224');

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `Student_ID` varchar(30) NOT NULL,
  `S_FirstName` varchar(50) NOT NULL,
  `S_LastName` varchar(50) NOT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Birthday` date DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Major` varchar(50) DEFAULT NULL,
  `Address` varchar(50) DEFAULT NULL,
  `Class_ID` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Student`
--

INSERT INTO `Student` (`Student_ID`, `S_FirstName`, `S_LastName`, `Gender`, `Birthday`, `Department`, `Major`, `Address`, `Class_ID`) VALUES
('123', 'Anny', 'J', 'Female', '1998-01-01', 'Business', 'Accounting', '7521 Belgrave Cove, Northgate, QLD, 4013', 'ACCT1'),
('236', 'Jone', 'W', 'Male', '1997-12-23', 'Business', 'Accounting', '7104 Legend Avenue, Waterfront Place, QLD, 4001', 'ACCT2'),
('354', 'Steven', 'K', 'Male', '1997-06-02', 'Business', 'Economics', '7402 Woodhall Lane, Eagle Farm, QLD, 4009', 'ECON1'),
('369', 'Iris', 'M', 'Female', '1999-07-20', 'Engineering', 'Information System', '9913 Shadowmoss Parkway,Waterfront Place,QLD,4001', 'IT1'),
('459', 'Jane', 'R', 'Female', '1995-10-01', 'Health', 'Health', '7206 Nikerton Street, Wintergarden, QLD, 4002', 'HEAL1'),
('521', 'Kate', 'P', 'Female', '1996-02-21', 'Medicine', 'Medicine', '579 Woodleaf Drive, Albion, QLD, 4010', 'MED1'),
('606', 'KJ', 'J', 'Male', '1997-09-04', 'Medicine', 'Pharmacy', '3611 Oaks Avenue, Spring Hill, QLD, 4000', 'PHAR1'),
('701', 'Zack', 'H', 'Male', '1998-10-16', 'Engineering', 'Data Science', '9170 Wethersfield Way,Rothwell,QLD,4022', 'DS1'),
('714', 'Olivia', 'K', 'Female', '1997-05-01', 'Science', 'Physics', '5450 Cd Smith Way,New Farm,QLD,4005', 'PHY1'),
('842', 'Jeff', 'J', 'Male', '1994-04-28', 'Science', 'Chemical', '2277 Old Bridge Parkway,Rothwell,QLD,4022', 'CHEM1');

-- --------------------------------------------------------

--
-- Table structure for table `Teacher`
--

CREATE TABLE `Teacher` (
  `Teacher_ID` varchar(50) NOT NULL,
  `Teacher_Name` varchar(50) NOT NULL,
  `T_Mail` varchar(100) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Education_Experience` varchar(1000) DEFAULT NULL,
  `Dept_ID` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Teacher`
--

INSERT INTO `Teacher` (`Teacher_ID`, `Teacher_Name`, `T_Mail`, `Department`, `Education_Experience`, `Dept_ID`) VALUES
('T128', 'Stephen Birch', 'stephen.birch@uq.edu.au', 'Business', 'Accounting Phd graduating from ANU', 1),
('T136', 'Inma Beaumont', 'i.beaumont@uq.edu.au', 'Business', 'Accounting Phd graduating from ANU', 1),
('T152', 'Sandy Brauer', 's.brauer@uq.edu.au', 'Business', 'Economics Phd graduating from NYU', 1),
('T224', 'Laurie Buys', 'l.buys@uq.edu.au', 'Science', 'Chemical Phd graduating from UCLA', 2),
('T239', 'John Cairney', 'j.cairney@uq.edu.au', 'Science', 'Physics Phd graduating from Griffth', 2),
('T303', 'Jason Connor', 'cysar@uq.edu.au', 'Engineering', 'Data Science Phd graduating from MIT', 3),
('T386', 'Neil Cottrell', 'n.cottrell@uq.edu.au', 'Engineering', 'IT Phd graduating from MIT', 3),
('T416', 'Andrew Cresswell', 'hos@hms.uq.edu.au', 'Medicine', 'Medicine Phd graduating from Cambridge', 4),
('T460', 'Sharon Doyle', 's.doyle1@uq.edu.au\r\n', 'Medicine', 'Pharmacy Phd graduating from Oxford', 4),
('T511', 'Derek Arnold', 'habs.adr@uq.edu.au', 'Health', 'Health Phd graduating from UQ', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Class`
--
ALTER TABLE `Class`
  ADD PRIMARY KEY (`Class_ID`,`Dept_ID`);

--
-- Indexes for table `Compulsory`
--
ALTER TABLE `Compulsory`
  ADD PRIMARY KEY (`Course_ID`),
  ADD KEY `Teacher_ID` (`Teacher_ID`);

--
-- Indexes for table `Department`
--
ALTER TABLE `Department`
  ADD PRIMARY KEY (`Dept_ID`);

--
-- Indexes for table `Enrollment`
--
ALTER TABLE `Enrollment`
  ADD KEY `FK_En` (`Student_ID`),
  ADD KEY `FK_E` (`Course_ID`);

--
-- Indexes for table `Project`
--
ALTER TABLE `Project`
  ADD PRIMARY KEY (`Project_ID`,`Teacher_ID`);

--
-- Indexes for table `Selective`
--
ALTER TABLE `Selective`
  ADD PRIMARY KEY (`Course_ID`),
  ADD KEY `Teacher_ID` (`Teacher_ID`);

--
-- Indexes for table `Student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`Student_ID`),
  ADD KEY `Class_ID` (`Class_ID`);

--
-- Indexes for table `Teacher`
--
ALTER TABLE `Teacher`
  ADD PRIMARY KEY (`Teacher_ID`),
  ADD KEY `Dept_ID` (`Dept_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Compulsory`
--
ALTER TABLE `Compulsory`
  ADD CONSTRAINT `Compulsory_ibfk_1` FOREIGN KEY (`Teacher_ID`) REFERENCES `Teacher` (`Teacher_ID`);

--
-- Constraints for table `Enrollment`
--
ALTER TABLE `Enrollment`
  ADD CONSTRAINT `FK_E` FOREIGN KEY (`Course_ID`) REFERENCES `Compulsory` (`Course_ID`),
  ADD CONSTRAINT `FK_En` FOREIGN KEY (`Student_ID`) REFERENCES `Student` (`Student_ID`);

--
-- Constraints for table `Selective`
--
ALTER TABLE `Selective`
  ADD CONSTRAINT `Selective_ibfk_1` FOREIGN KEY (`Teacher_ID`) REFERENCES `Teacher` (`Teacher_ID`);

--
-- Constraints for table `Student`
--
ALTER TABLE `Student`
  ADD CONSTRAINT `Student_ibfk_1` FOREIGN KEY (`Class_ID`) REFERENCES `Class` (`Class_ID`);

--
-- Constraints for table `Teacher`
--
ALTER TABLE `Teacher`
  ADD CONSTRAINT `Teacher_ibfk_1` FOREIGN KEY (`Dept_ID`) REFERENCES `Department` (`Dept_ID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
