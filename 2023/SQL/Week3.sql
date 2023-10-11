-- Preppin' Data | 2023 | Week 3

-- Part 1

WITH TRANSACTIONS AS (
  SELECT 
    DECODE(
      "Online or In-Person", 1, 'Online', 
      2, 'In-Person'
    ) AS "Online or In-Person", 
    QUARTER(
      TO_TIMESTAMP(
        "Transaction Date", 'dd/mm/yyyy hh:mi:ss'
      )
    ) AS "Quarter", 
    SUM("Value") AS "Value" 
  FROM 
    RA_PD_2023_WK1 
  WHERE 
    "Transaction Code" LIKE 'DSB%' 
  GROUP BY 
    1, 
    2
), 

TARGETS AS (
  SELECT 
    "Online or In-Person", 
    "Quarterly Targets", 
    "Quarter" 
  FROM 
    RA_PD_2023_WK3 UNPIVOT(
      "Quarterly Targets" FOR "Quarter" IN ("Q1", "Q2", "Q3", "Q4")
    )
) 

SELECT 
  A."Online or In-Person", 
  A."Quarter", 
  "Value", 
  "Quarterly Targets", 
  "Value" - "Quarterly Targets" AS "Variance to Target" 
FROM 
  TRANSACTIONS A 
  JOIN TARGETS B ON A."Online or In-Person" = B."Online or In-Person" 
  AND A."Quarter" = LTRIM(B."Quarter", 'Q');
