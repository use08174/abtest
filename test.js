const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Load your HTML content
    const htmlContent = `
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopping Mall Product Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        header {
            background-color: #333;
            color: white;
            padding: 10px 20px;
            text-align: center;
        }
        .container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
        }
        .product {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .product img {
            max-width: 100%;
            border-radius: 10px;
        }
        .product-details {
            flex: 1;
            padding: 20px;
            border-radius: 10px;
        }
        .product-details h2 {
            margin-top: 0;
        }
        .price {
            color: #E63946;
            font-size: 24px;
            margin: 10px 0;
        }
        .description {
            margin: 15px 0;
        }
        button {
            background-color: #FF6347;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
        }
        button:hover {
            background-color: #FF4500;
        }
    </style>
</head>
<body>

<header>
    <h1>Shopping Mall</h1>
</header>

<div class="container">
    <div class="product">
        <div class="product-image">
            <img src="https://example.com/high-quality-backpack.jpg" alt="Stylish Backpack">
        </div>
        <div class="product-details">
            <h2>Stylish Backpack</h2>
            <p class="price">$49.99</p>
            <p class="description">
                This stylish and durable backpack is perfect for everyday use. With plenty of space for your essentials, it’s great for work, school, or travel.
            </p>
            <button>Add to Cart</button>
        </div>
    </div>
</div>

</body>
</html>

    `;
    await page.setContent(htmlContent);

    // Take a screenshot
    await page.screenshot({ path: 'screenshot.png' });

    await browser.close();
})();