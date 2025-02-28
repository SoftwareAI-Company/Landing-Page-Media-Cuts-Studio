function updatePriceFields(price) {
    const orderSummaryPriceEl = document.querySelector('.frame-6556 ._103-00');
    if (orderSummaryPriceEl) {
      orderSummaryPriceEl.textContent = `$${price}`;
    }
    
    const discountedPriceEl = document.querySelector('.discounted-price');
    if (discountedPriceEl) {
      discountedPriceEl.textContent = `$${price}`;
    }
    
    const subtotalEl = document.querySelector('.block-order-summary-subtotal ._59');
    if (subtotalEl) {
      subtotalEl.textContent = `$${price}`;
    }
    const tax = 0.00;
    const totalEl = document.querySelector('.money-total ._69');
    if (totalEl) {
      const totalPrice = (parseFloat(price) + tax).toFixed(2);
      totalEl.textContent = `$${totalPrice}`;
    }
  }
  
document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const priceParam = urlParams.get("price");
    if (priceParam && !isNaN(priceParam)) {
      const priceValue = parseFloat(priceParam).toFixed(2);
      updatePriceFields(priceValue);
    }
  });
  