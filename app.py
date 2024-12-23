from flask import Flask,  jsonify, json , render_template, request, redirect, url_for, make_response, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions
CORS(app)  # Enable CORS for all routes

best_seller_products = [
    {"id": 12, "name": "Source Beauty", "Price": "EGP 429.78", "description": "Baby Powder Perfume", 
    "image": "https://sourcebeauty.com/cdn/shop/files/New-Baby-Powder_eefcc600-545f-4534-9c5d-b164ac97d464_750x.png?v=1719825197"},

    {"id": 13, "name": "Laque", "Price": "EGP 287.10", "description": "Don't Let It Slide: Lift & Hold Clear Brow Gel", 
    "image": "https://sourcebeauty.com/cdn/shop/products/Laque-Dont-Let-It-Slide--Lift-_-Hold_750x.png?v=1677864580"},

    {"id": 14, "name": "Rush Brush", "Price": "EGP 3,230", "description": "X6 Straightener", 
    "image": "https://sourcebeauty.com/cdn/shop/products/X6gray2_1000x.png?v=1679393470"},

    {"id": 15, "name": "Curlit", "Price": "EGP 245", "description": "Leave-In Conditioner for Wavy Hair", 
    "image": "https://sourcebeauty.com/cdn/shop/products/Curlit-leave-in-conditioner-1-Source-Beauty-Egypt_1000x.png?v=1695294370"},

    {"id": 16, "name": "Raw African", "Price": "EGP 175", "description": "Follicle Booster Eyelash Edition", 
    "image": "https://sourcebeauty.com/cdn/shop/products/Raw-African-Follicle-Booster-Eyelash-Edition-Source-Beauty-Egypt_1000x.png?v=1710666274"},

    {"id": 17, "name": "Godly Pride", "Price": "EGP 630", "description": "Holy Grail Hyaluronic Acid Moisturizing Cream", 
    "image": "https://sourcebeauty.com/cdn/shop/files/Godly-Pride-Holy-Grail-Hydrating-Cream-Source-Beauty-Egypt_5101d674-6f31-4eb6-8010-c394b18e9feb_1000x.png?v=1732783628"},   
    
    {"id": 18, "name": "ORB", "Price": "EGP 490", "description": "Sleek N' Fleek Hair Styling SET", 
    "image": "https://sourcebeauty.com/cdn/shop/files/ORB-Sleek-N_-Fleek-Hair-Styling-SET-Source-Beauty-Egypt_750x.png?v=1702454583"},
    
    {"id": 19, "name": "Godly Pride", "Price": "EGP 300", "description": "Tinted lip oil-to-gloss", 
    "image": "https://sourcebeauty.com/cdn/shop/files/Godly-Pride-Shade-101---Poetic-Justice---Hint-of-Pink-Source-Beauty-Egypt_d401a97e-3fb2-41c0-9179-9172b4eb8ad3_1000x.png?v=1725473063"},
]

customer_reviews = [
    {
    "name": "Yara Ali","comment": "Amazing product! Great quality and fast shipping.","rating": 5, 
    "avatar_url": "data:image/jpeg;base64,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"
    },
    {
    "name": "Mai Waleed","comment": "I love this store! The items are always top-notch.", "rating": 4,
    "avatar_url": "data:image/jpeg;base64,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"},
    {
    "name": "Gina Adel","comment": "Good service, but shipping took a little longer than expected.", "rating": 3, 
    "avatar_url": "data:image/jpeg;base64,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"
    }
]

products = [
    {"id": 1,"name": "Cosmo APPE Moisturizing Cream", "Price": "EGP 250", "Size": "75ml" , 
    "image": "images/product1.jpg"},
    
    {"id": 2, "name": "Derma Soft Plus Cream", "Price": "EGP 160","Size": "100ml",  
     "image": "images/product2.webp"},
    
    {"id": 3, "name": "COSMO APPE Facial Wash All Skin Types Pump", "Price": "EGP 300", "Size": "250ml",
     "image": "images/product3.jpg"},
    
    {"id": 4, "name": "Macro Topi-Gent Cleansing Foam", "Price": "EGP 252","Size": "150ml",
     "image": "images/product4.jpg"},
    
    {"id": 5, "name": "COSMO APPE Light Tinted Sunscreen spf 50+", "Price": "EGP 450","Size": "60ml", 
     "image":"images/product5.jpg"},
    
    {"id": 6, "name": "Bobana sunscreen gel", "Price": "EGP 122","Size": "150ml",
     "image": "images/product6.jpg"},
    
    {"id": 7, "name": "Cleo Super Serum Hyaluronic acid + Niacinamide", "Price": "EGP 400","Size": "25ml", 
     "image": "images/product7.jpg"},
    
    {"id": 8, "name": "Eva cosmetics", "Price": "EGP 184","Size": "370ml", 
     "image": "images/product8.jpg"},
    
    {"id": 9, "name": "Eva Skin Care Shower Cream", "Price": "EGP 79","Size": "250ml", 
     "image": "images/product9.jpg"},
    
    {"id": 10, "name": "Eva Skin Care Senses Body Splash", "Price": "EGP 79","Size": "250ml", 
     "image": "images/product10.webp"},
    
    {"id": 11, "name": "Eva Skin Care Senses body splash - Red Glamour", "Price": "EGP 165","Size": "240ml", 
     "image": "images/product11.webp"},

    {"id": 12, "name": "Source Beauty Perfume", "Price": "EGP 429.78", "Size": "100ml", 
    "image": "images/product12.webp"},

    {"id": 13, "name": "Laque Brow Gel", "Price": "EGP 287.10", "Size": "9.5ml", 
    "image": "images/product13.webp"},

    {"id": 14, "name": "Rush Brush Hair Straightener", "Price": "EGP 3,230",
    "image": "images/product14.webp"},

    {"id": 15, "name": "Curlit Leave-In Conditioner", "Price": "EGP 245",  "Size": "200ml", 
    "image": "images/product15.webp"},

    {"id": 16, "name": "Raw African Eyelash Serum", "Price": "EGP 175", "Size": "5ml", 
    "image": "images/product16.webp"},

    {"id": 17, "name": "Godly Pride Moisturizing Cream", "Price": "EGP 630", "Size": "50ml", 
    "image": "images/product17.webp"},   
    
    {"id": 18, "name": "ORB Hair Styling SET", "Price": "EGP 490", "Size": "30ml", 
    "image": "images/product18.webp"},
    
    {"id": 19, "name": "Godly Pride Lip Gloss", "Price": "EGP 300", "Size": "30ml", 
    "image": "images/product19.webp"},
]

products_details = [
    {"id": 1, "name": "Cosmo APPE Moisturizing Cream", "Price": "EGP 250", "Size": "75ml",
    "Description": "APPE Cream is designed for daily care and gentle protection of your skin from Dryness & inflammation. Natural components build a reliable, permeable barrier, which allows your skin to breathe while remaining tender and smooth.", 
    "image": "images/product1.jpg",
    "content":"cosmo APPE Moisturizing Cream is a hydrating cream designed to relieve dryness and reduce inflammation on the skin. This nourishing cream is formulated with soothing ingredients to restore the skin's moisture balance, providing immediate hydration while calming irritated or inflamed areas"
    },
    
    {"id": 2, "name": "Derma Soft Plus Cream", "Price": "EGP 160","Size": "100ml", 
    "Description": "Dermasoft Plus Cream is characterized by an anti-aging formula with high moisturizing properties because it contains phytocollagen.", 
    "image": "images/product2.webp",
    "content":"It works to protect the skin from dehydration, regenerate skin cells,and resist signs of aging and signs of wrinkles. And because it contains antioxidants, it works to fight wrinkles in the skin. Vitamin E, the main ingredient in Derma Soft cream, also protects the skin from sunburn and harmful weather factors "
    },
    
    {"id": 3, "name": "COSMO APPE Facial Wash All Skin Types Pump", "Price": "EGP 300", "Size": "250ml",
    "Description": "Nourishing Cleansing Gel, sulfate-freeand, 250 ML Bottle for daily use.", 
    "image": "images/product3.jpg",
    "content":"Pamper yourself with this lightweight cleanser that deeply cleanses, leaving your skin feeling refreshed and revitalized. With its soothing formula, it removes impurities without stripping away essential moisture ."
    },
    
    {"id": 4, "name": "Macro Topi-Gent Cleansing Foam", "Price": "EGP 252","Size": "150ml", 
    "Description":"3 offers from EGP 400.00", 
    "image": "images/product4.jpg",
    "content":"A common benefit of facial cleansing is the removal of dirt, oil, and other unwanted debris. Throughout the day the skin on your face is continually covered with bacteria, pollutants, viruses, dirt, and old (dead) skin cells. Daily facial washing removes these impurities to give the skin a fresh look."
    },
    
    {"id": 5, "name": "COSMO APPE Light Tinted Sunscreen spf 50+", "Price": "EGP 450","Size": "60ml", 
    "Description":"APPE® Light Tinted Sunscreen spf 50+UVA & UVB Protection, with Caviar Extract", 
    "image":"images/product5.jpg",
    "content":"Tinted Sunscreen SPF 50+ – Cosmo Appe. Experience UVA & UVB protection, fast absorption, deep moisturizing, and a tint with Cosmo Appe's Tinted Sunscreen. A premium sun protection solution that will subtly even out skin tone, providing a natural appearance while protecting from the sun. Evens out skin tone."
    },
    
    {"id": 6, "name": "Bobana sunscreen gel", "Price": "EGP 122","Size": "150ml", 
    "Description":"This product is to be used once a day", 
    "image": "images/product6.jpg",
    "content":"A lightweight, anti-shine, and fast-absorbing gel formula by Bobana that provides superior broad-spectrum UVA & UVB protection with SPF of 50+ against sunburn, premature skin aging, and pigmentation caused by sun exposure."
    },
    
    {"id": 7, "name": "Cleo Super Serum Hyaluronic acid + Niacinamide", "Price": "EGP 400","Size": "25ml", 
    "Description":"Cleo Super Serum combines the benefits of Hyaluronic Acid and Niacinamide into a powerful daily skin booster.", 
    "image": "images/product7.jpg",
    "content":"Highlights Plumping – younger skin ,Secures hydration, Smooth texture,Reduce fine lines and wrinkles,For external use only. Keep out of reach of young children. Store in a cool, dry place away from direct heat or sunlight."
    },
    
    {"id": 8, "name": "Eva cosmetics", "Price": "EGP 184","Size": "370ml", 
    "Description":"Optimum Care Recipe Radiance Blend Lotion For Normal Skin - Marshmallow Scent",
    "image": "images/product8.jpg",
    "content":"A lotion is a topical preparation, applied to the skin with bare hands or cotton wool, with the intent to moisturise and/or treat the skin. Most body lotions are meant to simply keep the skin soft, smooth and healthy, but they can also have anti-ageing properties and contain fragrances ."
    },
    
    {"id": 9, "name": "Eva Skin Care Shower Cream", "Price": "EGP 79","Size": "250ml", 
    "Description": "It has been packed under hygienic conditions, making it highly beneficial for you. Please read the instructions on the package before use.", 
    "image": "images/product9.jpg",
    "content":"Eva Skin Care Body Lotion, with its special care, provides your skin with silky, smooth and luxurious feel. Its deep formula, enriched with moisturizing ingredients, works as water magnet that binds with water molecules and holds them in the skin cells. Vaseline softens and smoothes the skin."
    },
    
    {"id": 10, "name": "Eva Skin Care Senses Body Splash ", "Price": "EGP 79","Size": "250ml", 
    "Description": "Hold the bottle 10cm away from the body and spray it on your clothes or skin. Use some on your collar bones and wrist for long-lasting freshness. Use daily to bring your mysterious vibe alive, every time", 
    "image": "images/product10.webp",
    "content":"Gold Spell Body Splash – Eva Cosmetics. In The Cloudes Mist from Eva  Cosmetics is a sophisticated choice for women. It blends the delightful scents of flowers, a hint of pear, and sweet praline to create a beautiful and vibrant aroma. It is specifically crafted to evoke the warmth of summer and the comfort of autumn."
    },
    
    {"id": 11, "name": "Eva Skin Care Senses body splash - Red Glamour", "Price": "EGP 165","Size": "240ml",
    "Description": "Opens with the fresh and tangy smell that adds a touch of warmth and sensuality to the overall scent. Fragrance notes: Mandarin, Vanilla, Jasmine, blackcurrant and Malton Flower.", 
    "image": "images/product11.webp",
    "content":"Opens with the fresh and tangy smell that adds a touch of warmth and sensuality to the overall scent. Fragrance notes: Mandarin, Vanilla, Jasmine, blackcurrant and Malton Flower."
    },
    
    {"id": 12, "name": "Source Beauty", "price": "EGP 429.78", "Size": "100ml", 
    "Description": "Baby Powder Perfume", 
    "image": "images/product12.webp",
    "content":"Experience the blissful nostalgia of baby powder with our Baby Powder Perfume. This gentle fragrance radiates cozy freshness, transporting you to a realm of contentment. Embrace the softness and serenity of a newborn with this soothing, feminine scent. Let the comforting cleanliness and delicate notes of pink and powder melt away your worries."
    },
    
    {"id": 13, "name": "Laque", "Price": "EGP 287.10", "Size": "9.5ml", 
    "Description": "Don't Let It Slide: Lift & Hold Clear Brow Gel", 
    "image": "images/product13.webp",
    "content":"Set your brows in place with this Laque Don’t Let It Slide: Lift & Hold Brow Gel. The lightweight formula will help define and give an extra firm hold to your brows that will set them in place all day long. The soft texture makes it easy to apply and can also be used to help set baby hairs in place."
    },
    
    {"id": 14, "name": "Rush Brush", "Price": "EGP 3,230", 
    "Description": "X6 Straightener", 
    "image": "images/product14.webp",
    "content":"The RUSHBRUSH® X6 Straightener will be your new favorite straightening tool. Whether you're seeking a sleek look or the perfect beachy waves; this straightener can do it all. The wider plate is designed to achieve bigger, thicker, and longer hair."
    }, 

    {"id": 15, "name": "Curlit", "Price": "EGP 245", "Size": "200ml", 
    "Description": "Leave-In Conditioner for Wavy Hair", 
    "image": "images/product15.webp",
    "content":"Curlit presents an exceptional leave-in conditioner designed specifically for wavy hair. Formulated without silicone and parabens, this product provides optimal hydration, taming frizz and accentuating the natural waves of your hair. With the breakthrough ingredient Crodzaosoft, this leave-in conditioner has been clinically tested to effectively nurture and repair damaged hair, while also depositing Vitamin E for added nourishment."
    },
    
    {"id": 16, "name": "Raw African", "Price": "EGP 175", "Size": "5ml", 
    "Description": "Follicle Booster Eyelash Edition", 
    "image": "images/product16.webp",
    "content":"Discover the magic of naturally fuller lashes with Raw African Follicle Booster Eyelash Edition. This gentle gel formula is a dream for sensitive eyes, being free from fragrances and harsh chemicals. It's designed to nourish and strengthen your lashes from the root, enhancing their health and encouraging the growth of thicker lashes. This amazing Follicle Booster not only fortifies lashes against breakage but also stimulates blood circulation for faster, more vibrant growth."
    },
    
    {"id": 17, "name": "Godly Pride", "Price": "EGP 630", "Size": "50ml", 
    "Description": "Holy Grail Hyaluronic Acid Moisturizing Cream", 
    "image": "images/product17.webp",
    "content":"This Holy Grail Hyaluronic Acid Moisturizing Cream has a rich texture that provides moisture and hydration. Empowered with niacinamide to provide plumpness and rose water to act as a natural toner, this cream will leave you with balanced glowing skin."
    },   
    
    {"id": 18, "name": "ORB", "Price": "EGP 490", "Size": "30ml", 
    "Description": "Sleek N' Fleek Hair Styling SET", 
    "image": "images/product18.webp",
    "content":"Get ready to transform your hair game with the Sleek N' Fleek Hair Styling Kit! This ultimate styling tool is here to banish flyaways and give you flawless, sleek locks that will turn heads. Our solid stick formula is packed with hydrating ingredients and natural beeswax, ensuring your hair stays in place all day long. And with the teasing brush included in this kit, you have complete control over any style you desire. Suitable for all hair types, this kit is a must-have for anyone who wants to achieve salon-quality results from the comfort of their own home. Get excited and get Sleek N' Fleek today!"
    },
    
    {"id": 19, "name": "Godly Pride", "Price": "EGP 300", "Size": "30ml", 
    "Description": "Tinted lip oil-to-gloss", 
    "image": "images/product19.webp",
    "content":"This revolutionary tinted oil-to-gloss from Godly Pride provides a soft, long-lasting layer of hydration while imparting a subtle, customizable hue for a natural look, it incredibly moisturizes the lips with its blend of oils."},
]

# Store users in a simple dictionary
# Format: {"username": {"password": "password"}}
users = {} 
# List to store user data
user_data = []

# Track viewed products in the session
def track_viewed_product(product_id):
    if 'viewed_products' not in session:
        session['viewed_products'] = []
    if product_id not in session['viewed_products']:
        session['viewed_products'].append(product_id)
        session.modified = True

# Get viewed products from session
def get_viewed_products():
    return session.get('viewed_products', [])

@app.route("/")
def index(): 
    # Get the list of viewed products from the session
    viewed_product_ids = get_viewed_products()  # Fetch viewed product IDs from the session
    viewed_products = [product for product in products if product['id'] in viewed_product_ids]  # Get the product details based on the viewed IDs
# Debugging: print session and viewed products
    print("Session viewed products:", session.get('viewed_products'))
    print("Viewed Products:", viewed_products)
    
    return render_template("index.html", viewed_products=viewed_products, best_seller_products=best_seller_products, customer_reviews=customer_reviews, products=products, products_details =products_details)  # Default for non-logged-in users
   

@app.route("/search")
def search():
    query = request.args.get('query')
    if not query:
        return redirect('/product')  # Redirect to products if no query is provided
    
    # Perform the search (case-insensitive)
    results = [product for product in products if query.lower() in product['name'].lower()]
    
    return render_template('search_results.html', query=query, results=results)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Server-side validations
        if not username or not username.isalpha():
            return jsonify(success=False, message="Invalid username. Use letters only.")
        if not email or "@" not in email:
            return jsonify(success=False, message="Invalid email. Must contain '@'.")
        
        # Enhanced password validation
        import re
        password_regex = re.compile(r"^(?=.*[A-Z])(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d]{8,}$")
        if not password or not password_regex.match(password):
            return jsonify(
                success=False,
                message="Password must be at least 8 characters long, contain at least one uppercase letter, and include both letters and numbers."
            )
        if password != confirm_password:
            return jsonify(success=False, message="Passwords do not match.")
        if username in users:
            return jsonify(success=False, message="Username already exists.")

        # Save user to dictionary
        users[username] = {"email": email, "password": password}

        return jsonify(success=True, message="Sign-up successful!")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember")

        # Validate user credentials
        if not username or not password:
            return "Username and Password are required.", 400
        if username not in users or users[username]["password"] != password:
            return "Invalid username or password.", 400

        # Create a response object and set cookies
        response = make_response(redirect(url_for("index")))
        if remember:
            response.set_cookie("username", username, max_age=30 * 24 * 60 * 60)  # 30 days
        else:
            response.set_cookie("username", username)  # Session cookie

        return response

    return render_template("login.html")

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    response.delete_cookie("username")  # Remove the login cookie
    return response

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/product")
def product_page():
    username = request.cookies.get("username")
    # Pass the products to the products page
    if username:
        return render_template("product.html", products=products, username=username)
    return render_template("product.html", products=products)

@app.route("/product/<int:product_id>")
def product_details(product_id):
    try:
        selected_product = next(product for product in products_details if product["id"] == product_id)
        # Track the viewed product
        track_viewed_product(product_id)
        # Debugging: print the viewed product ID to ensure it's being tracked
        print(f"Viewed Product ID: {product_id}")
        return render_template("product-details.html", product=selected_product)
    except StopIteration:
        # Handle the case where the product is not found
        return render_template("404.html"), 404

@app.route("/rate-product/<int:product_id>", methods=["POST"])
def rate_product(product_id):
    data = request.get_json()
    rating = data.get("rating")

    if not rating or not (1 <= rating <= 5):
        return jsonify({"error": "Invalid rating"}), 400

    # يمكنك هنا حفظ التقييم في قاعدة البيانات
    print(f"Received rating {rating} for product {product_id}")

    return jsonify({"message": "Rating submitted successfully!"})

@app.route('/get-rating/<int:product_id>', methods=['GET'])
def get_rating(product_id):
    rating = rating.get(product_id)
    if rating:
        return jsonify({"rating": rating}), 200
    return jsonify({"rating": None}), 200

@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", [])
    quantity = request.json.get("quantity", 1)

    # Find the product by ID
    product = next((p for p in products_details if p["id"] == product_id), None)
    if product:
        # Convert price to a numerical value for easier calculation later
        price = float(product["Price"].replace("EGP", "").replace(",", "").strip())

        # Check if the product is already in the cart
        product_in_cart = next((item for item in cart if item["id"] == product_id), None)
        if product_in_cart:
            product_in_cart["quantity"] += quantity
        else:
            # Copy the product to avoid modifying the original list and add quantity
            product_copy = product.copy()
            product_copy["quantity"] = quantity
            product_copy["total_price"] = price * quantity  # Calculate total price for the quantity
            cart.append(product_copy)

        # Save the updated cart back to the session
        session["cart"] = cart
        return jsonify({"message": "Product added to cart", "cart": cart}), 200
    else:
        return jsonify({"error": "Product not found"}), 404
    

@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    quantity_to_remove = request.json.get("quantity", 1)
    
    # Find the product in the cart
    product_in_cart = next((item for item in cart if item["id"] == product_id), None)
    if product_in_cart:
        if product_in_cart["quantity"] > quantity_to_remove:
            product_in_cart["quantity"] -= quantity_to_remove
        else:
            cart = [item for item in cart if item["id"] != product_id]
        
        session["cart"] = cart
        return jsonify({"message": "Product removed from cart", "cart": cart}), 200
    
    return jsonify({"error": "Product not in cart"}), 404

@app.route("/cart", methods=["GET"])
def cart():
    cart = session.get("cart", [])
    return render_template("cart.html", cart=cart, best_seller_products=best_seller_products, products=products, products_details =products_details)

# الحصول على عدد المنتجات في السلة 
@app.route("/cart-count", methods=["GET"]) 
def cart_count(): 
    cart = session.get("cart", []) 
    return jsonify({"count": len(cart)}), 200 

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
@app.route('/submit', methods=['POST'])
def submit():
    # Get data from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    city = request.form.get('city')
    phone = request.form.get('phone')

    # Validate phone number
    if len(phone) != 11 or not phone.isdigit():
        return jsonify({"error": "Phone number must be exactly 11 digits"}), 400

    # Save user data to the list
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "city": city,
        "phone": phone
    }
    user_data.append(user)

    # Print user data to the terminal
    print("-" * 40)
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Address: {address}")
    print(f"City: {city}")
    print(f"Phone Number: {phone}")
    print("-" * 40)

    return jsonify(user)  # Return the saved user data

if __name__ == "__main__":
    app.run(debug=True)
