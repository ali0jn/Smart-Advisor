from unicode_tr.extras import slugify

cleaned = slugify('ABDÜLKERİM KAR').upper().replace('-', ' ')
print(cleaned)
