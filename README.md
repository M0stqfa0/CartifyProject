🛒 Cartify – Local Shopping System

Cartify is a desktop shopping app built with Python + CustomTkinter.
It demonstrates a multi-page GUI (Login, Register, Home, Cart, Profile, Admin Home) and a basic in-memory shopping flow: browse products, search, sort, add/remove from cart, and navigate between pages.

Features

Authentication pages: Login & Register UI (front-end validation hooks ready).

Home (Products) page: search, category filter, sort (name / price), scrollable product cards, add/remove quantities.

Cart & Profile navigation: passes selected items to the Cart page and supports viewing the Profile page.

Responsive layout: frames center content and stretch horizontally when the window is resized.

Local data: product data stored in products.json (easy to edit / extend).

Custom, reusable widgets: EntryWidget and ComboboxWidget in utils.py to keep UI code consistent.

```
Cartify/
│
├── main.py                # App entry + frame controller
├── login_frame.py         # Login UI 
├── register_frame.py      # Register UI 
├── user_home.py           # Home / browsing page 
├── cart_page.py           # Cart page 
├── profile_frame.py       # Profile page
├── theme.py               # Colors, fonts, constants
├── images/                # All icons 
├── admin_home.py          # Admin page, for editing and adding products
├── user_data.json         # Users data
├── products.json          # Product data 
└── README.md              # This file
```

Contributors & Roles

Mostafa Yasser — UI/UX, front-end implementation, CustomTkinter interface and styling, integration of pages.

Yousef Said — Admin page features and related functionality (admin workflows, admin-side product management).

Esraa Ahmed — Core algorithms and logic (sorting, search behavior, business logic, and main functional algorithms).
