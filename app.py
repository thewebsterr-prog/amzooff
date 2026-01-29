import React, { useState, useMemo, useEffect } from 'react';
import { 
  Search, ShoppingCart, Menu, Star, ArrowLeft, Heart, Home, 
  Package, User, Plus, Minus, Trash2, CheckCircle, Filter, X, 
  ChevronRight, MapPin, CreditCard, Truck 
} from 'lucide-react';

// --- Mock Data ---

const CATEGORIES = ["All", "Electronics", "Fashion", "Home", "Books", "Toys"];

const PRODUCTS = [
  {
    id: 1,
    title: "Wireless Noise Cancelling Headphones",
    price: 299.99,
    rating: 4.8,
    reviews: 1240,
    category: "Electronics",
    image: "/api/placeholder/400/400",
    description: "Industry-leading noise cancelling with Dual Noise Sensor technology. Next-level music with Edge-AI. Up to 30-hour battery life with quick charging.",
    userReviews: [
      { user: "Alex D.", rating: 5, comment: "Best headphones I've ever owned. Silence is golden." },
      { user: "Sarah M.", rating: 4, comment: "Great sound, but a bit heavy on the ears after 4 hours." }
    ]
  },
  {
    id: 2,
    title: "Smart 4K UHD TV - 55 Inch",
    price: 449.00,
    rating: 4.6,
    reviews: 890,
    category: "Electronics",
    image: "/api/placeholder/400/300",
    description: "Experience your favorite movies and TV shows in stunning 4K UHD resolution. Smart TV features built-in with voice remote.",
    userReviews: [
        { user: "MovieBuff99", rating: 5, comment: "Picture quality is insane for this price point." }
    ]
  },
  {
    id: 3,
    title: "Men's Cotton Casual Shirt",
    price: 24.99,
    rating: 4.2,
    reviews: 450,
    category: "Fashion",
    image: "/api/placeholder/300/400",
    description: "100% Cotton, regular fit. Perfect for casual wear or semi-formal occasions. Breathable fabric for all-day comfort.",
    userReviews: []
  },
  {
    id: 4,
    title: "Stainless Steel Chef Knife",
    price: 45.50,
    rating: 4.9,
    reviews: 210,
    category: "Home",
    image: "/api/placeholder/400/400",
    description: "High-carbon stainless steel blade. Ergonomic handle for comfort and control. Sharpest edge in its class.",
    userReviews: [
        { user: "ChefBoy", rating: 5, comment: "Razor sharp out of the box." }
    ]
  },
  {
    id: 5,
    title: "Best Seller Novel: The Silent Echo",
    price: 14.99,
    rating: 4.7,
    reviews: 3300,
    category: "Books",
    image: "/api/placeholder/300/450",
    description: "A gripping mystery thriller that will keep you on the edge of your seat until the very last page.",
    userReviews: []
  },
  {
    id: 6,
    title: "Robot Vacuum Cleaner",
    price: 199.99,
    rating: 4.3,
    reviews: 560,
    category: "Home",
    image: "/api/placeholder/400/400",
    description: "Automated cleaning with smart mapping. Works on carpets and hard floors. App controlled.",
    userReviews: [
        { user: "CleanFreak", rating: 3, comment: "Gets stuck under my sofa sometimes." }
    ]
  }
];

// --- Components ---

const StarRating = ({ rating, count }) => (
  <div className="flex items-center text-sm">
    <div className="flex text-yellow-500">
      {[...Array(5)].map((_, i) => (
        <Star key={i} size={14} fill={i < Math.floor(rating) ? "currentColor" : "none"} stroke="currentColor" className={i < Math.floor(rating) ? "" : "text-gray-300"} />
      ))}
    </div>
    {count !== undefined && <span className="text-gray-500 ml-1 text-xs">({count})</span>}
  </div>
);

const Button = ({ children, onClick, variant = "primary", className = "", disabled = false }) => {
  const baseStyle = "w-full py-3 rounded-lg font-medium transition-colors active:scale-95 duration-200 flex items-center justify-center";
  const variants = {
    primary: "bg-yellow-400 text-black hover:bg-yellow-500 shadow-sm",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    outline: "border border-gray-300 text-gray-700 hover:bg-gray-50",
    danger: "bg-red-50 text-red-600 hover:bg-red-100",
    ghost: "bg-transparent hover:bg-gray-100"
  };
  
  return (
    <button 
      onClick={onClick} 
      disabled={disabled}
      className={`${baseStyle} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
    >
      {children}
    </button>
  );
};

export default function App() {
  // --- State ---
  const [view, setView] = useState("home"); // home, product, cart, checkout, orders, orderSuccess
  const [activeProduct, setActiveProduct] = useState(null);
  const [cart, setCart] = useState([]);
  const [orders, setOrders] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // --- Derived State ---
  const filteredProducts = useMemo(() => {
    return PRODUCTS.filter(p => {
      const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = selectedCategory === "All" || p.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [searchQuery, selectedCategory]);

  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  const cartCount = cart.reduce((sum, item) => sum + item.qty, 0);

  // --- Handlers ---
  
  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, qty: item.qty + 1 } : item);
      }
      return [...prev, { ...product, qty: 1 }];
    });
  };

  const removeFromCart = (id) => {
    setCart(prev => prev.filter(item => item.id !== id));
  };

  const updateQty = (id, delta) => {
    setCart(prev => prev.map(item => {
      if (item.id === id) {
        return { ...item, qty: Math.max(1, item.qty + delta) };
      }
      return item;
    }));
  };

  const handleCheckout = () => {
    const newOrder = {
      id: `ORD-${Math.floor(Math.random() * 10000)}`,
      date: new Date().toLocaleDateString(),
      items: [...cart],
      total: cartTotal,
      status: "Processing"
    };
    setOrders([newOrder, ...orders]);
    setCart([]);
    setView("orderSuccess");
  };

  // --- Views ---

  const Header = () => (
    <div className="bg-[#232f3e] text-white p-3 sticky top-0 z-50 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <Menu className="cursor-pointer" onClick={() => setIsMenuOpen(!isMenuOpen)} />
          <span className="font-bold text-xl tracking-tight">AmznClone</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="relative cursor-pointer" onClick={() => setView("cart")}>
            <ShoppingCart size={24} />
            {cartCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-yellow-400 text-black text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full">
                {cartCount}
              </span>
            )}
          </div>
        </div>
      </div>
      
      {/* Search Bar */}
      <div className="relative">
        <input
          type="text"
          placeholder="Search products..."
          className="w-full p-2.5 pl-10 rounded-md text-gray-800 focus:outline-none"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <Search className="absolute left-3 top-3 text-gray-500" size={18} />
      </div>

      {/* Categories (Horizontal Scroll) */}
      {view === "home" && (
        <div className="flex gap-2 mt-3 overflow-x-auto pb-1 no-scrollbar text-sm">
          {CATEGORIES.map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`whitespace-nowrap px-4 py-1.5 rounded-full transition-colors ${
                selectedCategory === cat 
                  ? "bg-white text-gray-900 font-medium" 
                  : "bg-gray-700 text-gray-300 hover:bg-gray-600"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      )}
    </div>
  );

  const BottomNav = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-2 px-6 flex justify-between z-50 text-xs text-gray-600">
      <button 
        onClick={() => setView("home")} 
        className={`flex flex-col items-center ${view === "home" ? "text-cyan-700 font-bold" : ""}`}
      >
        <Home size={22} className="mb-1" />
        Home
      </button>
      <button 
        onClick={() => setView("cart")} 
        className={`flex flex-col items-center ${view === "cart" ? "text-cyan-700 font-bold" : ""}`}
      >
        <ShoppingCart size={22} className="mb-1" />
        Cart
      </button>
      <button 
        onClick={() => setView("orders")} 
        className={`flex flex-col items-center ${view === "orders" ? "text-cyan-700 font-bold" : ""}`}
      >
        <Package size={22} className="mb-1" />
        Orders
      </button>
      <button className="flex flex-col items-center opacity-60">
        <User size={22} className="mb-1" />
        Profile
      </button>
    </div>
  );

  const HomeView = () => (
    <div className="p-3 pb-20 grid grid-cols-2 gap-3 bg-gray-100 min-h-screen">
      {filteredProducts.length === 0 ? (
        <div className="col-span-2 text-center py-10 text-gray-500">
          <p>No products found matching "{searchQuery}"</p>
        </div>
      ) : (
        filteredProducts.map(product => (
          <div 
            key={product.id} 
            className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 flex flex-col cursor-pointer hover:shadow-md transition-shadow"
            onClick={() => {
              setActiveProduct(product);
              setView("product");
            }}
          >
            <div className="w-full h-32 bg-gray-100 mb-3 rounded-md flex items-center justify-center overflow-hidden">
               {/* Placeholder for real images */}
               <Package className="text-gray-300" size={40} />
            </div>
            <div className="flex-1 flex flex-col">
              <h3 className="text-sm font-medium line-clamp-2 leading-tight mb-1">{product.title}</h3>
              <StarRating rating={product.rating} count={product.reviews} />
              <div className="mt-auto pt-2">
                <span className="text-xs text-gray-500 block mb-1">{product.category}</span>
                <span className="text-lg font-bold">${product.price.toFixed(2)}</span>
                <span className="text-xs text-gray-400 ml-2 line-through">${(product.price * 1.2).toFixed(2)}</span>
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );

  const ProductDetailView = () => (
    <div className="bg-white min-h-screen pb-20">
      <div className="p-4 border-b border-gray-100 flex items-center gap-3">
        <button onClick={() => setView("home")} className="p-1 hover:bg-gray-100 rounded-full">
          <ArrowLeft size={24} />
        </button>
        <span className="font-medium text-lg">Product Details</span>
      </div>
      
      <div className="p-4">
        {/* Mock Image */}
        <div className="w-full h-64 bg-gray-50 rounded-lg flex items-center justify-center mb-6">
          <Package size={80} className="text-gray-300" />
        </div>
        
        <div className="flex justify-between items-start mb-2">
           <h1 className="text-xl font-bold text-gray-800 leading-snug flex-1">{activeProduct.title}</h1>
           <Heart className="text-gray-400 ml-4 hover:text-red-500 cursor-pointer" />
        </div>
        
        <div className="flex items-center gap-2 mb-4">
           <StarRating rating={activeProduct.rating} />
           <span className="text-blue-600 text-sm font-medium">{activeProduct.reviews} ratings</span>
        </div>

        <div className="mb-6">
          <span className="text-red-700 text-sm font-medium">Deal of the Day</span>
          <div className="flex items-baseline gap-3">
             <span className="text-3xl font-bold">${activeProduct.price}</span>
             <span className="text-gray-500 line-through text-sm">List: ${(activeProduct.price * 1.2).toFixed(2)}</span>
          </div>
        </div>

        <div className="space-y-3 mb-8">
           <Button onClick={() => addToCart(activeProduct)}>Add to Cart</Button>
           <Button variant="secondary" onClick={() => { addToCart(activeProduct); setView("cart"); }}>Buy Now</Button>
        </div>

        <div className="border-t border-gray-100 pt-4">
          <h3 className="font-bold text-lg mb-2">Description</h3>
          <p className="text-gray-600 text-sm leading-relaxed">{activeProduct.description}</p>
        </div>
        
        <div className="border-t border-gray-100 pt-4 mt-6">
          <h3 className="font-bold text-lg mb-4">Customer Reviews</h3>
          {activeProduct.userReviews.length > 0 ? (
            activeProduct.userReviews.map((review, idx) => (
              <div key={idx} className="mb-4 p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                   <div className="w-6 h-6 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold text-white">
                     {review.user[0]}
                   </div>
                   <span className="text-sm font-medium">{review.user}</span>
                </div>
                <div className="flex mb-1 text-yellow-500"><Star size={12} fill="currentColor" /></div>
                <p className="text-sm text-gray-600">"{review.comment}"</p>
              </div>
            ))
          ) : (
            <p className="text-gray-400 text-sm italic">No reviews yet.</p>
          )}
        </div>
      </div>
    </div>
  );

  const CartView = () => (
    <div className="bg-gray-50 min-h-screen pb-32">
      <div className="p-4 bg-white shadow-sm flex items-center gap-3 sticky top-0 z-10">
        <button onClick={() => setView("home")}><ArrowLeft /></button>
        <h2 className="text-xl font-bold">Shopping Cart ({cartCount})</h2>
      </div>

      <div className="p-3 space-y-3">
        {cart.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400">
            <ShoppingCart size={64} className="mb-4 opacity-20" />
            <p className="text-lg font-medium">Your cart is empty</p>
            <Button className="mt-6 w-48" variant="secondary" onClick={() => setView("home")}>
              Start Shopping
            </Button>
          </div>
        ) : (
          <>
            {cart.map(item => (
              <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 flex gap-4">
                <div className="w-20 h-20 bg-gray-100 rounded flex-shrink-0 flex items-center justify-center">
                  <Package className="text-gray-400" />
                </div>
                <div className="flex-1">
                  <h4 className="text-sm font-medium line-clamp-2 mb-1">{item.title}</h4>
                  <p className="text-lg font-bold mb-2">${item.price}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 bg-gray-50 rounded-md p-1">
                      <button onClick={() => item.qty > 1 ? updateQty(item.id, -1) : removeFromCart(item.id)} className="p-1 hover:bg-white rounded shadow-sm transition-all"><Minus size={14} /></button>
                      <span className="text-sm font-medium w-4 text-center">{item.qty}</span>
                      <button onClick={() => updateQty(item.id, 1)} className="p-1 hover:bg-white rounded shadow-sm transition-all"><Plus size={14} /></button>
                    </div>
                    <button onClick={() => removeFromCart(item.id)} className="text-gray-400 hover:text-red-500">
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
            
            {/* Subtotal Section */}
            <div className="bg-white p-4 rounded-lg shadow-sm mt-4">
              <div className="flex justify-between mb-2 text-gray-600">
                <span>Subtotal</span>
                <span>${cartTotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between mb-2 text-gray-600">
                <span>Shipping</span>
                <span className="text-green-600">FREE</span>
              </div>
              <div className="flex justify-between text-xl font-bold border-t pt-3 mt-2">
                <span>Total</span>
                <span>${cartTotal.toFixed(2)}</span>
              </div>
              
              <Button className="mt-6" onClick={() => setView("checkout")}>
                Proceed to Checkout ({cartCount} items)
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );

  const CheckoutView = () => (
    <div className="bg-gray-50 min-h-screen pb-20">
      <div className="p-4 bg-white shadow-sm flex items-center gap-3 sticky top-0 z-10">
        <button onClick={() => setView("cart")}><ArrowLeft /></button>
        <h2 className="text-xl font-bold">Checkout</h2>
      </div>

      <div className="p-4 space-y-4">
        {/* Shipping Address Mock */}
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2 mb-3 text-gray-700 font-medium">
             <MapPin size={18} /> Shipping Address
          </div>
          <div className="pl-6 text-sm text-gray-600 leading-relaxed">
            <p className="font-bold text-black">Guest User</p>
            <p>123 Demo Street, App Apartment</p>
            <p>Silicon Valley, CA 94000</p>
            <p>United States</p>
          </div>
        </div>

        {/* Payment Method Mock */}
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2 mb-3 text-gray-700 font-medium">
             <CreditCard size={18} /> Payment Method
          </div>
          <div className="pl-6 flex items-center gap-3 p-3 border border-blue-100 bg-blue-50 rounded-md">
            <div className="w-8 h-5 bg-gray-800 rounded"></div>
            <div className="text-sm">
              <p className="font-bold">Mock Card ending in 1234</p>
              <p className="text-xs text-gray-500">Expires 12/28</p>
            </div>
            <CheckCircle className="ml-auto text-green-600" size={20} />
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <h3 className="font-bold mb-3">Order Summary</h3>
          <div className="space-y-2 text-sm text-gray-600">
             <div className="flex justify-between">
                <span>Items</span>
                <span>${cartTotal.toFixed(2)}</span>
             </div>
             <div className="flex justify-between">
                <span>Delivery</span>
                <span>$0.00</span>
             </div>
             <div className="flex justify-between font-bold text-black text-lg pt-2 border-t">
                <span>Order Total</span>
                <span className="text-red-700">${cartTotal.toFixed(2)}</span>
             </div>
          </div>
        </div>

        <Button onClick={handleCheckout} className="mt-4 shadow-lg">Place Order</Button>
        <p className="text-xs text-center text-gray-400 mt-2">By placing an order, you agree to the mock terms of use.</p>
      </div>
    </div>
  );

  const OrderSuccessView = () => (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
       <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
         <CheckCircle className="text-green-600" size={48} />
       </div>
       <h2 className="text-2xl font-bold mb-2">Order Placed!</h2>
       <p className="text-gray-500 mb-8">Thank you for your purchase. Your mock order has been confirmed.</p>
       
       <Button onClick={() => setView("orders")} variant="outline" className="mb-3">
         Track Order
       </Button>
       <Button onClick={() => setView("home")} variant="ghost">
         Continue Shopping
       </Button>
    </div>
  );

  const OrdersView = () => (
    <div className="bg-gray-50 min-h-screen pb-20">
      <div className="p-4 bg-white shadow-sm flex items-center gap-3 sticky top-0 z-10">
        <h2 className="text-xl font-bold">Your Orders</h2>
      </div>

      <div className="p-4 space-y-4">
        {orders.length === 0 ? (
          <div className="text-center py-20 text-gray-400">
             <Package size={48} className="mx-auto mb-3 opacity-30" />
             <p>No orders history found.</p>
          </div>
        ) : (
          orders.map(order => (
            <div key={order.id} className="bg-white rounded-lg shadow-sm overflow-hidden">
               <div className="bg-gray-100 p-3 flex justify-between items-center text-xs text-gray-600">
                  <div>
                    <span className="block font-bold text-gray-800">ORDER PLACED</span>
                    <span>{order.date}</span>
                  </div>
                  <div className="text-right">
                    <span className="block font-bold text-gray-800">TOTAL</span>
                    <span>${order.total.toFixed(2)}</span>
                  </div>
               </div>
               <div className="p-4">
                  <h4 className="font-bold text-lg text-green-700 mb-2 flex items-center gap-2">
                    <Truck size={18} /> {order.status}
                  </h4>
                  <p className="text-sm text-gray-500 mb-4">Arriving usually in 2 days</p>
                  
                  <div className="space-y-3">
                    {order.items.map((item, i) => (
                      <div key={i} className="flex gap-3">
                         <div className="w-12 h-12 bg-gray-100 rounded flex items-center justify-center flex-shrink-0">
                           <Package size={20} className="text-gray-400" />
                         </div>
                         <div className="text-sm">
                           <p className="font-medium line-clamp-1">{item.title}</p>
                           <p className="text-xs text-gray-500">Qty: {item.qty}</p>
                         </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 pt-3 border-t flex gap-3">
                    <button className="flex-1 py-2 text-sm border rounded-md hover:bg-gray-50 font-medium">Track Package</button>
                    <button className="flex-1 py-2 text-sm border rounded-md hover:bg-gray-50 font-medium">Buy Again</button>
                  </div>
               </div>
            </div>
          ))
        )}
      </div>
    </div>
  );

  return (
    <div className="font-sans text-gray-900 bg-gray-100 min-h-screen">
      <div className="max-w-md mx-auto bg-white min-h-screen shadow-2xl relative overflow-hidden">
        
        {/* Render Header only on Home or Product pages for "App-like" feel, customized for others */}
        {view === "home" && <Header />}
        
        <main className="min-h-screen">
          {view === "home" && <HomeView />}
          {view === "product" && <ProductDetailView />}
          {view === "cart" && <CartView />}
          {view === "checkout" && <CheckoutView />}
          {view === "orderSuccess" && <OrderSuccessView />}
          {view === "orders" && <OrdersView />}
        </main>

        {/* Bottom Navigation available on main tabs */}
        {(view === "home" || view === "cart" || view === "orders") && <BottomNav />}
      </div>
    </div>
  );
}
