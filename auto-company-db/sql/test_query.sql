-- Test query file

SELECT m.model_name, b.brand_name, v.vin
FROM Vehicle v
JOIN Model m ON v.model_id = m.model_id
JOIN Brand b ON m.brand_id = b.brand_id
LIMIT 10;

SELECT s.name AS supplier, COUNT(vp.vin) AS parts_used
FROM Supplier s
JOIN Part p ON s.supplier_id = p.supplier_id
JOIN Vehicle_Part vp ON p.part_id = vp.part_id
GROUP BY s.name
ORDER BY parts_used DESC;