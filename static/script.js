document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('orderForm');
    const typeRadios = document.querySelectorAll('input[name="type"]');
    const priceGroup = document.getElementById('priceGroup');
    const priceInput = document.getElementById('price');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const notificationArea = document.getElementById('notificationArea');

    // Toggle Price input based on Order Type
    typeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'LIMIT') {
                priceGroup.style.opacity = '1';
                priceGroup.style.pointerEvents = 'auto';
                priceInput.required = true;
                priceInput.placeholder = "e.g. 60000";
            } else {
                priceGroup.style.opacity = '0.5';
                priceGroup.style.pointerEvents = 'none';
                priceInput.required = false;
                priceInput.value = '';
                priceInput.placeholder = "Market Price";
            }
        });
    });

    // Handle Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Loading State
        submitBtn.disabled = true;
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        notificationArea.innerHTML = '';
        notificationArea.classList.add('hidden');

        // Gather Data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Convert string values appropriately
        data.symbol = data.symbol.toUpperCase();
        data.quantity = parseFloat(data.quantity);
        if (data.price) {
            data.price = parseFloat(data.price);
        } else {
            delete data.price;
        }

        try {
            const response = await fetch('/api/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                showNotification('success', 'Order Executed', 
                    `Order ID: ${result.data.orderId || 'N/A'}<br>Status: ${result.data.status || 'NEW'}`
                );
            } else {
                showNotification('error', 'Order Failed', result.error || 'An unknown error occurred.');
            }

        } catch (error) {
            showNotification('error', 'System Error', 'Could not connect to the trading bot server.');
            console.error(error);
        } finally {
            // Restore UI
            submitBtn.disabled = false;
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    function showNotification(type, title, message) {
        notificationArea.innerHTML = `
            <div class="notification ${type}">
                <div class="notification-title">${title}</div>
                <div class="notification-detail">${message}</div>
            </div>
        `;
        notificationArea.classList.remove('hidden');
    }
});
