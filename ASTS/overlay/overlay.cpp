#include <windows.h>
#include <dwmapi.h>
#include <iostream>

#pragma comment(lib, "dwmapi.lib")

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int main() {
    // Register the window class
    const char CLASS_NAME[] = "OverlayWindowClass";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);

    RegisterClass(&wc);

    // Create the window
    HWND hwnd = CreateWindowEx(
        WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST,
        CLASS_NAME,
        "Overlay",
        WS_POPUP,
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
        NULL, NULL, wc.hInstance, NULL
    );

    if (hwnd == NULL) {
        std::cerr << "Failed to create window" << std::endl;
        return 0;
    }

    // Set the window to be transparent
    SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA);
    MARGINS margins = { -1 };
    DwmExtendFrameIntoClientArea(hwnd, &margins);

    ShowWindow(hwnd, SW_SHOW);

    // Main message loop
    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);

            // Implement the drawing logic here
            HBRUSH brush = CreateSolidBrush(RGB(255, 0, 0)); // Red brush
            RECT rect = { 50, 50, 200, 200 }; // Rectangle coordinates
            FillRect(hdc, &rect, brush); // Draw the rectangle
            DeleteObject(brush);

            EndPaint(hwnd, &ps);
        } break;

        case WM_DESTROY: {
            PostQuitMessage(0);
        } return 0;

        default: {
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
        }
    }
    return 0;
}
