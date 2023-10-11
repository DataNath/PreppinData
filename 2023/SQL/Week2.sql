-- Preppin' Data | 2023 | Week 2

-- Part 1

SELECT 
  "Transaction ID", 
  'GB' || "Check Digits" || "SWIFT code" || REPLACE("Sort Code", '-', '') || "Account Number" AS "IBAN" 
FROM 
  RA_PD_2023_WK2_T A 
  JOIN RA_PD_2023_WK2_SC B ON A."Bank" = B."Bank";
