-- Preppin' Data | 2023 | Week 4

-- Part 1

WITH UNIONED AS (
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 01, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_JAN 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 02, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_FEB 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 03, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_MAR 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 04, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_APR 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 05, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_MAY 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 06, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_JUN 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 07, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_JUL 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 08, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_AUG 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 09, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_SEP 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 10, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_OCT 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 11, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_NOV 
  UNION 
  SELECT 
    *, 
    TO_CHAR(
      DATE_FROM_PARTS(2023, 12, "Joining Day"), 
      'dd/mm/yyyy'
    ) AS "JDR" 
  FROM 
    NP_PD_2023_WK4_DEC
) 
SELECT 
  "ID", 
  "Joining Date", 
  "Account Type", 
  "Date of Birth", 
  "Ethnicity" 
FROM 
  (
    SELECT 
      ROW_NUMBER() OVER (
        PARTITION BY ID 
        ORDER BY 
          "JDR"
      ) AS RN, 
      "ID", 
      "JDR" AS "Joining Date", 
      "ACCOUNT_TYPE" AS "Account Type", 
      TO_CHAR(
        TO_DATE("DATE_OF_BIRTH", 'mm/dd/yyyy'), 
        'dd/mm/yyyy'
      ) AS "Date of Birth", 
      "ETHNICITY" AS "Ethnicity" 
    FROM 
      UNIONED PIVOT (
        MAX("VALUE") FOR "DEMOGRAPHIC" IN (
          'Account Type', 'Date of Birth', 
          'Ethnicity'
        )
      ) AS A (
        ID, Joining_day, JDR, Account_Type, 
        Date_of_Birth, Ethnicity
      )
  ) 
WHERE 
  RN = 1;
