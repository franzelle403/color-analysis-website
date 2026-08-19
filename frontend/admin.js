const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("makeup-form");

const productList =
    document.getElementById("product-list");

const searchInput =
    document.getElementById("search");

const cancelEditButton =
    document.getElementById("cancel-edit");

const formTitle =
    document.getElementById("form-title");

let allProducts = [];


// --------------------------------
// LOAD DATABASE
// --------------------------------

async function loadProducts() {

    try {

        const response =
            await fetch(`${API_URL}/makeup`);

        const data =
            await response.json();

        allProducts =
            data.products || [];

        displayProducts(allProducts);

    } catch (error) {

        console.error(error);

        productList.innerHTML = `
            <p>
                Could not connect to the backend.
                Make sure FastAPI is running.
            </p>
        `;
    }
}


// --------------------------------
// DISPLAY DATABASE
// --------------------------------

function displayProducts(products) {

    productList.innerHTML = "";

    document.getElementById(
        "product-count"
    ).textContent =
        `${products.length} products`;

    if (products.length === 0) {

        productList.innerHTML = `
            <div class="empty-state">
                No makeup products found.
            </div>
        `;

        return;
    }


    products.forEach(product => {

        const card =
            document.createElement("div");

        card.className = "product-card";


        const image = product.image_url
            ? `
                <img
                    src="${product.image_url}"
                    alt="${product.product_name}"
                >
            `
            : `
                <div class="image-placeholder">
                    No image
                </div>
            `;


        card.innerHTML = `

            ${image}

            <div class="product-card-content">

                <span class="category">
                    ${product.category}
                </span>

                <h3>
                    ${product.brand}
                </h3>

                <p class="product-name">
                    ${product.product_name}
                </p>

                <p>
                    Shade:
                    <strong>
                        ${product.shade}
                    </strong>
                </p>

                <div class="tags">

                    <span>
                        ${product.season}
                    </span>

                    ${
                        product.undertone
                        ? `<span>${product.undertone}</span>`
                        : ""
                    }

                    ${
                        product.depth
                        ? `<span>${product.depth}</span>`
                        : ""
                    }

                    ${
                        product.chroma
                        ? `<span>${product.chroma}</span>`
                        : ""
                    }

                </div>

                <p class="price">
                    ₱${Number(
                        product.price || 0
                    ).toFixed(2)}
                </p>


                <div class="card-buttons">

                    <button
                        onclick="editProduct(${product.id})"
                        class="edit-button"
                    >
                        Edit
                    </button>


                    <button
                        onclick="deleteProduct(${product.id})"
                        class="delete-button"
                    >
                        Delete
                    </button>

                </div>

            </div>
        `;

        productList.appendChild(card);
    });
}


// --------------------------------
// ADD / UPDATE PRODUCT
// --------------------------------

form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const productId =
            document.getElementById(
                "product-id"
            ).value;


        const product = {

            brand:
                document.getElementById(
                    "brand"
                ).value,

            product_name:
                document.getElementById(
                    "product-name"
                ).value,

            category:
                document.getElementById(
                    "category"
                ).value,

            shade:
                document.getElementById(
                    "shade"
                ).value,

            season:
                document.getElementById(
                    "season"
                ).value,

            undertone:
                document.getElementById(
                    "undertone"
                ).value,

            depth:
                document.getElementById(
                    "depth"
                ).value,

            chroma:
                document.getElementById(
                    "chroma"
                ).value,

            price:
                Number(
                    document.getElementById(
                        "price"
                    ).value
                ) || 0,

            image_url:
                document.getElementById(
                    "image-url"
                ).value,

            buy_url:
                document.getElementById(
                    "buy-url"
                ).value
        };


        try {

            let response;


            if (productId) {

                response = await fetch(
                    `${API_URL}/makeup/${productId}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(product)
                    }
                );

            } else {

                response = await fetch(
                    `${API_URL}/makeup`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(product)
                    }
                );
            }


            const data =
                await response.json();


            if (!response.ok) {

                console.error(data);

                alert(
                    "Could not save product."
                );

                return;
            }


            resetForm();

            await loadProducts();


        } catch (error) {

            console.error(error);

            alert(
                "Could not connect to backend."
            );
        }
    }
);


// --------------------------------
// EDIT
// --------------------------------

function editProduct(id) {

    const product =
        allProducts.find(
            product => product.id === id
        );

    if (!product) {
        return;
    }


    document.getElementById(
        "product-id"
    ).value = product.id;


    document.getElementById(
        "brand"
    ).value = product.brand;


    document.getElementById(
        "product-name"
    ).value = product.product_name;


    document.getElementById(
        "category"
    ).value = product.category;


    document.getElementById(
        "shade"
    ).value = product.shade;


    document.getElementById(
        "season"
    ).value = product.season;


    document.getElementById(
        "undertone"
    ).value = product.undertone || "";


    document.getElementById(
        "depth"
    ).value = product.depth || "";


    document.getElementById(
        "chroma"
    ).value = product.chroma || "";


    document.getElementById(
        "price"
    ).value = product.price || "";


    document.getElementById(
        "image-url"
    ).value = product.image_url || "";


    document.getElementById(
        "buy-url"
    ).value = product.buy_url || "";


    formTitle.textContent =
        "Edit Makeup Product";


    cancelEditButton.hidden = false;


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// --------------------------------
// DELETE
// --------------------------------

async function deleteProduct(id) {

    const confirmed = confirm(
        "Delete this makeup product?"
    );

    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/makeup/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            alert(
                "Could not delete product."
            );

            return;
        }


        await loadProducts();


    } catch (error) {

        console.error(error);

        alert(
            "Could not connect to backend."
        );
    }
}


// --------------------------------
// CANCEL EDIT
// --------------------------------

cancelEditButton.addEventListener(
    "click",
    resetForm
);


function resetForm() {

    form.reset();

    document.getElementById(
        "product-id"
    ).value = "";

    formTitle.textContent =
        "Add Makeup Product";

    cancelEditButton.hidden = true;
}


// --------------------------------
// SEARCH
// --------------------------------

searchInput.addEventListener(
    "input",
    function() {

        const query =
            searchInput.value
                .toLowerCase()
                .trim();


        const filtered =
            allProducts.filter(product => {

                const searchableText = `
                    ${product.brand}
                    ${product.product_name}
                    ${product.category}
                    ${product.shade}
                    ${product.season}
                    ${product.undertone || ""}
                `.toLowerCase();


                return searchableText.includes(
                    query
                );
            });


        displayProducts(filtered);
    }
);


// --------------------------------
// START
// --------------------------------

loadProducts();