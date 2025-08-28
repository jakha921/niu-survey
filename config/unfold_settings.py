"""
Настройки Django Unfold для современного админ-интерфейса
"""

UNFOLD = {
    "SITE_TITLE": "NIU Survey Admin",
    "SITE_HEADER": "NIU Survey Management",
    "SITE_URL": "/",
    # "SITE_ICON": {
    #     "light": lambda request: "/static/niu-icon.svg",  # light mode
    #     "dark": lambda request: "/static/niu-icon-dark.svg",  # dark mode
    # },
    # "SITE_LOGO": {
    #     "light": lambda request: "/static/niu-logo-light.svg",  # light mode
    #     "dark": lambda request: "/static/niu-logo-dark.svg",  # dark mode
    # },
    
    # symbol
    # "SITE_SYMBOL": "restaurant_menu",
    
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "ENVIRONMENT": "apps.common.environment.environment_callback",
    "DASHBOARD_CALLBACK": "apps.common.dashboard.dashboard_callback",
    "THEME": "light",  # Force theme: "light" to match NIU design
    "LOGIN": {
        "image": lambda request: "/static/login-bg.jpg",
        "redirect_after": lambda request: "/admin/",
    },
    "STYLES": [
        lambda request: "/static/css/admin-extra.css",
    ],
    "SCRIPTS": [
        lambda request: "/static/js/admin-extra.js",
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 126",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99", 
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "249 250 251",
        },
        "primary": {
            "50": "240 253 244",
            "100": "220 252 231", 
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "0 128 0",  # NIU Green
            "600": "0 102 0", 
            "700": "0 77 0",
            "800": "0 51 0",
            "900": "0 26 0",
            "950": "0 13 0",
        }
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷", 
                "nl": "🇳🇱",
                "ru": "🇷🇺",
                "uz": "🇺🇿",
            },
        },
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": "NIU Dashboard",
                "separator": True,  # Top border
                "items": [

                    {
                        "title": "All Surveys",
                        "icon": "poll",
                        "model": "surveys.Survey",
                        "link": "/admin/surveys/survey/",
                    },
                ],
            },
            {
                "title": "User Management",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "model": "auth.User",
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "model": "auth.Group",
                    },
                ],
            },

        ],
    },
    # "TABS": [
    #     {
    #         "models": [
    #             "surveys.survey",
    #         ],
    #         "items": [
    #             {
    #                 "title": "All Surveys", 
    #                 "icon": "poll",
    #                 "link": "/admin/surveys/survey/",
    #             },
    #             {
    #                 "title": "Public View", 
    #                 "icon": "public",
    #                 "link": "/",
    #             },
    #         ],
    #     },
    # ],
} 