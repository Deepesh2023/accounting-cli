<template>
  <div class="max-w-5xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">Company Profile</h2>
      <UButton color="primary" icon="i-heroicons-check" class="shadow-md px-5">Save Changes</UButton>
    </div>

    <div class="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 overflow-hidden">
      <div class="p-6 lg:p-8">
        <div class="flex gap-8 flex-col lg:flex-row">
          <div class="lg:w-1/4 lg:text-center lg:border-r lg:border-gray-200 dark:lg:border-gray-700 lg:pr-8">
            <div class="mb-8">
              <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-3">Company Logo</label>
              <div class="inline-block relative">
                <div class="w-40 h-40 rounded-full bg-gray-100 dark:bg-gray-800 border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all duration-300 overflow-hidden">
                  <div class="text-center">
                    <Icon name="i-heroicons-photo" class="text-gray-400 text-2xl mx-auto" />
                    <span class="text-gray-400 text-xs font-bold block mt-1">ADD LOGO</span>
                  </div>
                </div>
                <p class="text-gray-400 text-xs mt-2">Click to upload your business logo</p>
              </div>
            </div>

            <div>
              <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-3">Payment QR Code</label>
              <div class="inline-block relative">
                <div class="w-40 h-40 bg-gray-100 dark:bg-gray-800 border-2 border-dashed border-gray-300 dark:border-gray-600 flex items-center justify-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all duration-300 overflow-hidden rounded-xl">
                  <div class="text-center">
                    <Icon name="i-heroicons-qr-code" class="text-gray-400 text-2xl mx-auto" />
                    <span class="text-gray-400 text-xs font-bold block mt-1">ADD QR</span>
                  </div>
                </div>
                <p class="text-gray-400 text-xs mt-2">Upload your UPI or Bank QR code</p>
              </div>
            </div>
          </div>

          <div class="lg:w-3/4">
            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6 mb-5">
              <h6 class="font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2 mb-5">
                <Icon name="i-heroicons-information-circle" class="w-4 h-4" />
                Basic Information
              </h6>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2 md:grid md:grid-cols-2 md:gap-4">
                  <div>
                    <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Business Name <span class="text-red-500">*</span></label>
                    <input type="text" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm" placeholder="e.g. Nectar Technologies">
                  </div>
                  <div>
                    <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Business Type</label>
                    <select class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm">
                      <option>Select Business Type</option>
                      <option>Retail</option>
                      <option>Wholesale</option>
                      <option>Manufacturing</option>
                      <option>Services</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Business Category</label>
                  <input type="text" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm" placeholder="e.g. IT Services">
                </div>
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Account Books Beginning Date</label>
                  <input type="date" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm">
                </div>
              </div>
            </div>

            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6 mb-5">
              <h6 class="font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2 mb-5">
                <Icon name="i-heroicons-map-pin" class="w-4 h-4" />
                Contact & Address
              </h6>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Phone Number</label>
                  <div class="flex">
                    <span class="bg-gray-100 dark:bg-gray-800 border-r border-gray-300 dark:border-gray-600 rounded-l-lg px-3 py-2.5 text-sm text-gray-500">+91</span>
                    <input type="text" class="flex-1 border-0 bg-gray-100 dark:bg-gray-800 rounded-r-lg px-3 py-2.5 text-sm">
                  </div>
                </div>
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Email Address</label>
                  <input type="email" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm" placeholder="company@example.com">
                </div>
                <div class="md:col-span-2">
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Address</label>
                  <input type="text" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm" placeholder="Street, City">
                </div>
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">State</label>
                  <select class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm">
                    <option>Select State</option>
                    <option value="Andhra Pradesh">Andhra Pradesh</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Kerala">Kerala</option>
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Tamil Nadu">Tamil Nadu</option>
                    <option value="Telangana">Telangana</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">Pincode</label>
                  <input type="text" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm">
                </div>
              </div>
            </div>

            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6 mb-5">
              <h6 class="font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2 mb-5">
                <Icon name="i-heroicons-document-text" class="w-4 h-4" />
                Statutory
              </h6>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="text-xs uppercase font-bold text-gray-500 dark:text-gray-400 block mb-1.5">GSTIN</label>
                  <input type="text" class="w-full border-0 bg-gray-100 dark:bg-gray-800 rounded-lg px-3 py-2.5 text-sm" placeholder="22AAAAA0000A1Z5">
                </div>
                <div class="flex items-end pb-2.5">
                  <label class="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" class="rounded border-gray-300">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Enable Party Netting</span>
                  </label>
                </div>
              </div>
            </div>

            <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-6">
              <h6 class="font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2 mb-5">
                <Icon name="i-heroicons-server-stack" class="w-4 h-4" />
                Data Backup & Restore
              </h6>
              <div class="flex gap-3">
                <UButton color="primary" variant="outline" icon="i-heroicons-arrow-down-tray">Export JSON</UButton>
                <UButton color="primary" variant="outline" icon="i-heroicons-arrow-up-tray">Import JSON</UButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
