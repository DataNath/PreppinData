-- Preppin' Data | 2023 | Week 1

-- Part 1

SELECT 
  SPLIT_PART("Transaction Code", '-', 1) AS "Bank", 
  SUM("Value") AS "Value"
FROM 
  RA_PD_2023_WK1 
GROUP BY 
  "Bank";

-- Part 2

SELECT 
  SPLIT_PART("Transaction Code", '-', 1) AS "Bank", 
  CASE "Online or In-Person" WHEN 1 THEN 'Online' ELSE 'In-Person' END AS "Online or In-Person", 
  DECODE(
    DAYOFWEEKISO(
      TO_TIMESTAMP(
        "Transaction Date", 'dd/mm/yyyy hh:mi:ss'
      )
    ), 
    1, 
    'Monday', 
    2, 
    'Tuesday', 
    3, 
    'Wednesday', 
    4, 
    'Thursday', 
    5, 
    'Friday', 
    6, 
    'Saturday', 
    7, 
    'Sunday'
  ) AS "Transaction Day", 
  SUM("Value") AS "Value" 
FROM 
  RA_PD_2023_WK1 
GROUP BY 
  "Bank", 
  "Online or In-Person", 
  "Transaction Day";
  
-- Part 3
  
SELECT 
  SPLIT_PART("Transaction Code", '-', 1) AS "Bank", 
  "Customer Code", 
  SUM("Value") AS "Value" 
FROM 
  RA_PD_2023_WK1 
GROUP BY 
  "Bank", 
  "Customer Code";
