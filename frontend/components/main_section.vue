<script setup lang="ts">
interface Product {
  id: number;
  name: string;
  description?: string;
  slug?: string;
  category?: string | number;
  brand?: string;
  connections?: string;
  price: number | string;
  sale_price?: number | string | null;
  stock?: number;
  is_active?: boolean;
  is_new?: boolean;
  is_featured?: boolean;
  image_url?: string;
}

const apiUrl = useRuntimeConfig().public.apiUrl;

const { data: recommendedProducts, error } = await useFetch<Product[]>(`${apiUrl}/api/products/recommendations/`);

if (error.value) {
  console.error("Failed to fetch recommendations:", error.value);
}

const categoryMapping: Record<string | number, string> = {
  '1': 'headphones',
  '2': 'speakers',
  '3': 'earphones',
};

// Manually navigate with window.location instead of Vue Router
// This is a more direct approach that bypasses potential router issues
const viewProductDetails = (productId: number, category: string | number): void => {
  console.log("View product details:", { productId, category });
  
  let categorySlug = '';
  
  // First check if we have a mapping for this category
  if (category && categoryMapping[category]) {
    categorySlug = categoryMapping[category];
  } else if (category) {
    // Convert to slug and use directly
    categorySlug = String(category).toLowerCase();
  } else {
    // Default fallback
    categorySlug = 'item';
  }
  
  // Use direct window location change instead of router.push
  const url = `/products/${categorySlug}/${productId}`;
  console.log("Navigating to:", url);
  window.location.href = url;
};

// Format price properly
const formatPrice = (price: number | string): string => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  return '$' + numPrice.toFixed(2);
};

// Force re-render on each component mount
const componentKey = Date.now();
</script>

<template>
  <section :key="componentKey" class="container mx-auto py-10 px-4">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold mb-2">Recommended For You</h2>
      <div class="w-16 h-1 bg-primary mx-auto"/>
    </div>

    <div v-if="recommendedProducts && recommendedProducts.length > 0" class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div 
        v-for="product in recommendedProducts" 
        :key="product.id" 
        class="card bg-base-100 shadow-md hover:shadow-xl transition-all duration-300"
      >
        <figure class="relative overflow-hidden">
          <img 
            :src="product.image_url || '/placeholder.png'" 
            :alt="product.name" 
            class="w-full h-48 object-cover transition-transform duration-500 hover:scale-105" 
          >
          <div class="absolute top-2 right-2">
            <!-- Show SALE badge if product has a sale_price -->
            <div v-if="product.sale_price" class="badge badge-accent">SALE</div>
          </div>
        </figure>

        <div class="card-body">
          <div class="flex flex-col">
            <h2 class="card-title text-lg">{{ product.name }}</h2>
            <h2 class="card-title text-sm text-primary">{{ product.brand}}</h2>
          </div>
          <p class="text-sm text-gray-600 line-clamp-2">{{ product.description || 'No description available' }}</p>
          
          <!-- Price display with sale price -->
          <div class="flex items-baseline gap-2 mt-2">
            <span v-if="product.sale_price" class="text-lg font-bold text-primary">
              {{ formatPrice(product.sale_price) }}
            </span>
            <span v-if="product.sale_price" class="text-sm text-base-content/60 line-through">
              {{ formatPrice(product.price) }}
            </span>
            <span v-else class="text-lg font-bold text-primary">
              {{ formatPrice(product.price) }}
            </span>
          </div>
          
          <div class="card-actions justify-end mt-4">
            <button 
              class="btn btn-primary btn-sm"
              @click="viewProductDetails(product.id, product.category || '')"
            >
              <Icon name="material-symbols:arrow-right-alt-rounded" class="mr-2"/>
              View Detail
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-gray-500">
      No recommended products available.
    </div>
  </section>
</template>