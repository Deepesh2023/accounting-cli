import { For } from 'solid-js'
import { createFileRoute } from '@tanstack/solid-router'
import { companyData, setCompanyData, indianStates } from '../lib/store'

export const Route = createFileRoute('/company')({ component: Company })

function Company() {
  function setField(field: string, value: string | boolean) {
    setCompanyData(field as any, value)
  }

  function handleLogo(input: HTMLInputElement) {
    const file = input.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
      setField('logo', e.target?.result as string)
    }
    reader.readAsDataURL(file)
  }

  function handleQR(input: HTMLInputElement) {
    const file = input.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
      setField('qr', e.target?.result as string)
    }
    reader.readAsDataURL(file)
  }

  function saveCompany() {
    alert('Company details saved successfully!')
  }

  function exportData() {
    const data = {
      transactions: [],
      partyList: [],
      stockList: [],
      quotationList: [],
      expenseList: [],
      companyData: { ...companyData },
    }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'accounting_backup.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  function importData(input: HTMLInputElement) {
    const file = input.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string)
        if (data.companyData) {
          setCompanyData(data.companyData)
        }
        alert('Data imported successfully!')
      } catch {
        alert('Invalid backup file.')
      }
    }
    reader.readAsText(file)
  }

  return (
    <div class="container-fluid py-4 space-y-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-bold mb-0">Company Profile</h2>
        <button
          onClick={saveCompany}
          class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded transition-colors"
        >
          Save Changes
        </button>
      </div>

      <div class="border-0 shadow-sm rounded-lg overflow-hidden p-5 bg-white">
        <div class="flex gap-8">
          {/* Logo & QR Section */}
          <div class="w-1/4 text-center border-r border-gray-200 pr-8">
            <div class="mb-5">
              <label class="block text-gray-500 text-xs uppercase font-bold mb-3">Company Logo</label>
              <div class="inline-block relative">
                <div
                  class="w-40 h-40 rounded-full bg-gray-100 flex items-center justify-center shadow-sm cursor-pointer overflow-hidden"
                  style="border: 2px dashed #dee2e6"
                  onClick={() => document.getElementById('comp_logo_input')?.click()}
                >
                  {companyData.logo ? (
                    <img src={companyData.logo} class="w-full h-full object-cover" />
                  ) : (
                    <div class="text-center">
                      <div class="text-gray-400 text-2xl mb-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="inline-block w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                      </div>
                      <span class="text-gray-500 text-xs font-bold">ADD LOGO</span>
                    </div>
                  )}
                </div>
                <input type="file" id="comp_logo_input" class="hidden" accept="image/*" onChange={(e) => handleLogo(e.currentTarget)} />
              </div>
              <p class="text-gray-500 text-xs mt-2">Click to upload your business logo</p>
            </div>

            <div class="mt-5">
              <label class="block text-gray-500 text-xs uppercase font-bold mb-3">Payment QR Code</label>
              <div class="inline-block relative">
                <div
                  class="w-40 h-40 bg-gray-100 flex items-center justify-center shadow-sm cursor-pointer overflow-hidden"
                  style="border: 2px dashed #dee2e6; border-radius: 12px"
                  onClick={() => document.getElementById('comp_qr_input')?.click()}
                >
                  {companyData.qr ? (
                    <img src={companyData.qr} class="w-full h-full object-cover" />
                  ) : (
                    <div class="text-center">
                      <div class="text-gray-400 text-2xl mb-1">
                        <svg xmlns="http://www.w3.org/2000/svg" class="inline-block w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" /></svg>
                      </div>
                      <span class="text-gray-500 text-xs font-bold">ADD QR</span>
                    </div>
                  )}
                </div>
                <input type="file" id="comp_qr_input" class="hidden" accept="image/*" onChange={(e) => handleQR(e.currentTarget)} />
              </div>
              <p class="text-gray-500 text-xs mt-2">Upload your UPI or Bank QR code</p>
            </div>
          </div>

          {/* Form Section */}
          <div class="w-3/4">
            {/* Basic Information */}
            <div class="mb-6">
              <h6 class="text-sm font-bold text-gray-600 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" /></svg>
                Basic Information
              </h6>
              <div class="grid grid-cols-2 gap-4">
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">
                    Business Name <span class="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={companyData.name}
                    onInput={(e) => setField('name', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                    placeholder="e.g. Nectar Technologies"
                  />
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Business Type</label>
                  <select
                    value={companyData.type}
                    onChange={(e) => setField('type', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Select Business Type</option>
                    <option value="Retail">Retail</option>
                    <option value="Wholesale">Wholesale</option>
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="Services">Services</option>
                  </select>
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Business Category</label>
                  <input
                    type="text"
                    value={companyData.category}
                    onInput={(e) => setField('category', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                    placeholder="e.g. IT Services"
                  />
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Account Books Beginning Date</label>
                  <input
                    type="date"
                    value={companyData.start_date}
                    onInput={(e) => setField('start_date', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Contact & Address */}
            <div class="mb-6">
              <h6 class="text-sm font-bold text-gray-600 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                Contact & Address
              </h6>
              <div class="grid grid-cols-2 gap-4">
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Phone Number</label>
                  <div class="flex">
                    <span class="inline-flex items-center px-3 bg-gray-100 border-0 text-sm text-gray-500 rounded-l">+91</span>
                    <input
                      type="text"
                      value={companyData.phone}
                      onInput={(e) => setField('phone', e.currentTarget.value)}
                      class="flex-1 border-0 bg-gray-100 rounded-r px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                    />
                  </div>
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Email ID</label>
                  <input
                    type="email"
                    value={companyData.email}
                    onInput={(e) => setField('email', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
                <div class="col-span-2">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Business Address</label>
                  <textarea
                    value={companyData.address}
                    onInput={(e) => setField('address', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                    rows="2"
                    placeholder="Full Address..."
                  />
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">State</label>
                  <select
                    value={companyData.state}
                    onChange={(e) => setField('state', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    <option value="">Select State</option>
                    <For each={indianStates.filter((s) => s !== 'Select State')}>
                      {(s) => <option value={s}>{s}</option>}
                    </For>
                  </select>
                </div>
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">Pincode</label>
                  <input
                    type="text"
                    value={companyData.pincode}
                    onInput={(e) => setField('pincode', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Statutory & Preferences */}
            <div class="mb-6">
              <h6 class="text-sm font-bold text-gray-600 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                Statutory & Preferences
              </h6>
              <div class="grid grid-cols-2 gap-4">
                <div class="col-span-2 md:col-span-1">
                  <label class="block text-gray-500 text-xs uppercase font-bold mb-1">GSTIN</label>
                  <input
                    type="text"
                    value={companyData.gstin}
                    onInput={(e) => setField('gstin', e.currentTarget.value)}
                    class="w-full border-0 bg-gray-100 rounded px-3 py-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
                    placeholder="Enter GSTIN"
                  />
                </div>
                <div class="col-span-2 md:col-span-1 flex items-center">
                  <div class="flex items-center gap-3">
                    <input
                      type="checkbox"
                      id="comp_netting"
                      checked={companyData.netting_enabled}
                      onChange={(e) => setField('netting_enabled', e.currentTarget.checked)}
                      class="w-10 h-5 accent-blue-600 cursor-pointer"
                    />
                    <div>
                      <label for="comp_netting" class="font-bold text-sm cursor-pointer">Enable Party Netting</label>
                      <p class="text-gray-500 text-xs">Standard Financial Presentation</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Data Backup & Restore */}
            <div>
              <h6 class="text-sm font-bold text-gray-600 mb-3 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                Data Backup & Restore
              </h6>
              <div class="grid grid-cols-2 gap-4 mt-1">
                <div class="col-span-2 md:col-span-1">
                  <div class="p-4 bg-gray-50 rounded text-center border border-green-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-green-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                    <h6 class="font-bold">Export Backup</h6>
                    <p class="text-gray-500 text-xs">Download all your accounting data securely as a JSON file.</p>
                    <button
                      onClick={exportData}
                      class="w-full mt-2 px-3 py-1.5 text-sm font-bold text-green-600 border border-green-600 rounded hover:bg-green-50 transition-colors"
                    >
                      Export Data
                    </button>
                  </div>
                </div>
                <div class="col-span-2 md:col-span-1">
                  <div class="p-4 bg-gray-50 rounded text-center border border-blue-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-blue-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                    <h6 class="font-bold">Import Backup</h6>
                    <p class="text-gray-500 text-xs">Restore your data from a previously downloaded JSON file.</p>
                    <input
                      type="file"
                      id="import_file"
                      class="hidden"
                      accept=".json"
                      onChange={(e) => importData(e.currentTarget)}
                    />
                    <button
                      onClick={() => document.getElementById('import_file')?.click()}
                      class="w-full mt-2 px-3 py-1.5 text-sm font-bold text-blue-600 border border-blue-600 rounded hover:bg-blue-50 transition-colors"
                    >
                      Import Data
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
