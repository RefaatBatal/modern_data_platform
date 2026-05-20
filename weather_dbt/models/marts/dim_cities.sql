WITH cities AS (
    SELECT DISTINCT
        city,
        latitude,
        longitude
    FROM {{ ref('stg_weather') }}
)

SELECT
    city,
    latitude,
    longitude,
    CURRENT_TIMESTAMP as created_at
FROM cities