# CleanTrack - UX/UI Design Guidelines

## Design Philosophy

CleanTrack's design prioritizes **clarity, efficiency, and confidence** for healthcare professionals working in fast-paced environments. Our design decisions are guided by three core principles:

1. **Trust Through Transparency**: Users should always know the state of compliance
2. **Speed Through Simplicity**: Common tasks should be achievable in <30 seconds
3. **Safety Through Validation**: Prevent errors before they happen

---

## Visual Design System

### Color Palette

#### Primary Colors
```
Blue (#2563eb)
- Primary actions
- Links
- Focus states
- Brand identity
RGB: 37, 99, 235
Usage: Buttons, navigation, important CTAs
```

#### Status Colors
```
Success Green (#10b981)
- Compliant status
- Completed actions
- Positive feedback
RGB: 16, 185, 129
Usage: ✓ checkmarks, success badges, compliant equipment

Warning Yellow (#f59e0b)
- Due soon alerts
- Caution messages
- Attention needed
RGB: 245, 158, 11
Usage: ⚠ warnings, due-soon badges

Danger Red (#ef4444)
- Overdue status
- Critical alerts
- Error messages
RGB: 239, 68, 68
Usage: ✗ errors, overdue badges, critical alerts

Info Blue (#3b82f6)
- Informational messages
- Tips and hints
- Neutral status
RGB: 59, 130, 246
Usage: 💡 tips, info boxes
```

#### Neutral Colors
```
Gray Scale
- Gray 900 (#111827): Primary text
- Gray 700 (#374151): Secondary text
- Gray 500 (#6b7280): Tertiary text, disabled
- Gray 300 (#d1d5db): Borders, dividers
- Gray 100 (#f3f4f6): Backgrounds, cards
- Gray 50 (#f9fafb): Page background
```

### Typography

#### Font Family
```css
/* System font stack for optimal performance */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             Roboto, Oxygen, Ubuntu, Cantarell,
             'Helvetica Neue', sans-serif;
```

#### Type Scale
```css
/* Headers */
h1: 36px / 2.25rem, font-weight: 700, line-height: 1.2
h2: 30px / 1.875rem, font-weight: 600, line-height: 1.3
h3: 24px / 1.5rem, font-weight: 600, line-height: 1.4
h4: 20px / 1.25rem, font-weight: 600, line-height: 1.5
h5: 16px / 1rem, font-weight: 600, line-height: 1.5

/* Body */
Large: 18px / 1.125rem, font-weight: 400, line-height: 1.6
Base: 16px / 1rem, font-weight: 400, line-height: 1.6
Small: 14px / 0.875rem, font-weight: 400, line-height: 1.5
XSmall: 12px / 0.75rem, font-weight: 400, line-height: 1.4

/* Special */
Code/Serial: Monospace, 14px, font-weight: 500
Caption: 12px, font-weight: 400, color: gray-500
```

### Spacing System

**8px Base Grid**
```
4px: xs (0.25rem) - Tight spacing
8px: sm (0.5rem) - Compact spacing
12px: md (0.75rem) - Default spacing
16px: lg (1rem) - Standard spacing
24px: xl (1.5rem) - Section spacing
32px: 2xl (2rem) - Large spacing
48px: 3xl (3rem) - Major sections
64px: 4xl (4rem) - Page sections
```

### Border Radius
```css
Small: 4px (0.25rem) - Buttons, badges
Medium: 6px (0.375rem) - Cards, inputs
Large: 8px (0.5rem) - Modals, containers
XLarge: 12px (0.75rem) - Hero sections
Full: 9999px - Pills, avatars
```

### Shadows
```css
/* Elevation levels */
sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
md: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1)
xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1)

/* Focus ring */
focus: 0 0 0 3px rgba(37, 99, 235, 0.2)
```

---

## Component Library

### Buttons

#### Variants
```html
<!-- Primary -->
<button class="btn btn-primary">
  Log Cleaning
</button>
Style: bg-blue-600, text-white, hover:bg-blue-700
Usage: Main actions, form submissions

<!-- Secondary -->
<button class="btn btn-secondary">
  Cancel
</button>
Style: bg-gray-200, text-gray-900, hover:bg-gray-300
Usage: Secondary actions, cancel

<!-- Danger -->
<button class="btn btn-danger">
  Delete
</button>
Style: bg-red-600, text-white, hover:bg-red-700
Usage: Destructive actions

<!-- Ghost -->
<button class="btn btn-ghost">
  View Details
</button>
Style: bg-transparent, text-blue-600, hover:bg-blue-50
Usage: Tertiary actions, links
```

#### Sizes
```css
Small: padding 8px 16px, font-size 14px
Medium: padding 12px 24px, font-size 16px (default)
Large: padding 16px 32px, font-size 18px
```

#### States
- **Default**: Normal appearance
- **Hover**: Slightly darker background
- **Active/Pressed**: Even darker, slight scale (0.98)
- **Focus**: Blue outline ring
- **Disabled**: 50% opacity, cursor not-allowed
- **Loading**: Spinner icon, disabled state

### Form Inputs

#### Text Input
```html
<input type="text" class="input" placeholder="Serial Number">
```
```css
Style:
- Border: 1px solid gray-300
- Padding: 12px 16px
- Font-size: 16px
- Border-radius: 6px
- Focus: border-blue-500, shadow-focus

States:
- Default: gray border
- Focus: blue border + shadow
- Error: red border + red text helper
- Disabled: gray-100 background, cursor not-allowed
- Success: green border (after validation)
```

#### Select Dropdown
```html
<select class="select">
  <option>All Locations</option>
</select>
```
- Chevron down icon on right
- Same styling as text input
- Highlight selected option in dropdown

#### Checkbox
```html
<input type="checkbox" id="step1">
<label for="step1">Power off equipment</label>
```
```css
Style:
- Size: 20px × 20px
- Border: 2px solid gray-400
- Checked: bg-blue-600, white checkmark
- Focus: blue outline ring
```

#### Radio Button
```css
Style:
- Size: 20px × 20px circle
- Border: 2px solid gray-400
- Selected: bg-blue-600, white dot
- Focus: blue outline ring
```

### Status Badges

```html
<!-- Compliant -->
<span class="badge badge-success">✓ Compliant</span>

<!-- Due Soon -->
<span class="badge badge-warning">⚠ Due Soon</span>

<!-- Overdue -->
<span class="badge badge-danger">✗ Overdue</span>

<!-- Inactive -->
<span class="badge badge-gray">Inactive</span>
```

```css
Style:
- Padding: 4px 12px
- Font-size: 12px
- Font-weight: 600
- Border-radius: 9999px
- Display: inline-flex
- Align-items: center
- Gap: 4px (icon + text)
```

### Cards

```html
<div class="card">
  <div class="card-header">
    <h3>GE Ultrasound Unit 1</h3>
    <span class="badge badge-success">✓</span>
  </div>
  <div class="card-body">
    <p>Serial: US-001-DEMO</p>
    <p>Location: Main Building</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">Log Cleaning</button>
  </div>
</div>
```

```css
Style:
- Background: white
- Border: 1px solid gray-200
- Border-radius: 8px
- Padding: 24px
- Shadow: sm
- Hover: shadow-md (if interactive)
```

### Alerts

```html
<!-- Critical -->
<div class="alert alert-danger">
  <svg class="alert-icon">🔴</svg>
  <div class="alert-content">
    <h4>Critical: Overdue Cleaning</h4>
    <p>Ventilator Unit A is overdue by 8 hours</p>
  </div>
  <button class="alert-close">×</button>
</div>
```

```css
Variants:
- Danger: bg-red-50, border-red-200, text-red-900
- Warning: bg-yellow-50, border-yellow-200, text-yellow-900
- Success: bg-green-50, border-green-200, text-green-900
- Info: bg-blue-50, border-blue-200, text-blue-900

Style:
- Padding: 16px
- Border: 1px solid
- Border-radius: 6px
- Display: flex
- Gap: 12px
```

### Modal/Dialog

```css
Overlay:
- Background: rgba(0, 0, 0, 0.5)
- Position: fixed, full screen
- Z-index: 1000

Modal:
- Background: white
- Border-radius: 12px
- Shadow: xl
- Max-width: 600px (small), 800px (medium), 1000px (large)
- Position: centered
- Padding: 32px

Header:
- Font-size: 24px
- Font-weight: 600
- Border-bottom: 1px solid gray-200
- Padding-bottom: 16px

Body:
- Padding: 24px 0
- Max-height: 70vh
- Overflow-y: auto

Footer:
- Border-top: 1px solid gray-200
- Padding-top: 16px
- Buttons: right-aligned, gap 12px
```

### Tables

```css
Style:
- Border: 1px solid gray-200
- Border-radius: 8px
- Overflow: hidden

Header:
- Background: gray-50
- Font-weight: 600
- Padding: 12px 16px
- Border-bottom: 2px solid gray-200
- Sticky: top 0 (if scrollable)

Rows:
- Padding: 16px
- Border-bottom: 1px solid gray-100
- Hover: background gray-50

States:
- Sortable: cursor pointer, hover effect on header
- Selected: background blue-50
```

---

## Icon System

### Icon Library
**Heroicons** (https://heroicons.com/) or **Material Icons**

### Icon Sizes
```css
xs: 16px
sm: 20px
md: 24px (default)
lg: 32px
xl: 48px
```

### Usage Guidelines
- Always pair with text for clarity (except well-known icons)
- Use consistent icons for same actions across app
- Ensure 4.5:1 contrast ratio with background

### Common Icons
```
✓ Checkmark: Success, completed, approved
✗ X: Error, failed, closed
⚠ Warning: Caution, due soon
🔔 Bell: Notifications, alerts
📷 Camera: Photo upload
📄 Document: Reports, files
⚙ Gear: Settings
👤 User: Profile, account
🔍 Magnify: Search
📊 Chart: Analytics, dashboard
📍 Pin: Location
⏱ Clock: Time, schedule
```

---

## Layout Patterns

### Dashboard Layout
```
┌─────────────────────────────────────────────────┐
│ Header (60px fixed)                             │
├─────────────────────────────────────────────────┤
│ │                                               │
│ │ Main Content Area                             │
│ │ (responsive grid)                             │
│ │                                               │
│ │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│ │ │ Card │ │ Card │ │ Card │ │ Card │         │
│ │ └──────┘ └──────┘ └──────┘ └──────┘         │
│ │                                               │
│ │ ┌───────────────────┐ ┌──────────────────┐   │
│ │ │ Chart             │ │ Recent Activity  │   │
│ │ └───────────────────┘ └──────────────────┘   │
│ │                                               │
└─────────────────────────────────────────────────┘

Grid: 12 columns
Gap: 24px
Max-width: 1400px
Padding: 24px
```

### List View Layout
```
┌─────────────────────────────────────────────────┐
│ Header + Filters (sticky)                       │
├─────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────┐ │
│ │ Item Card 1                                 │ │
│ └─────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────┐ │
│ │ Item Card 2                                 │ │
│ └─────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────┐ │
│ │ Item Card 3                                 │ │
│ └─────────────────────────────────────────────┘ │
│                                                   │
│ Pagination                                        │
└─────────────────────────────────────────────────┘

Max-width: 1200px
Padding: 24px
Gap between cards: 16px
```

### Form Layout
```
┌─────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────┐ │
│ │ Step Indicator                              │ │
│ │ ●━━━○━━━○━━━○                              │ │
│ └─────────────────────────────────────────────┘ │
│                                                   │
│ ┌─────────────────────────────────────────────┐ │
│ │ Form Section 1                              │ │
│ │ [Input fields]                              │ │
│ └─────────────────────────────────────────────┘ │
│                                                   │
│ ┌─────────────────────────────────────────────┐ │
│ │ Form Section 2                              │ │
│ │ [Input fields]                              │ │
│ └─────────────────────────────────────────────┘ │
│                                                   │
│ [← Back] [Cancel] [Continue →]                  │
└─────────────────────────────────────────────────┘

Max-width: 800px (single column)
Padding: 32px
Sections: separated by 24px
```

---

## Responsive Breakpoints

```css
/* Mobile First Approach */
/* Base: 320px - 767px (Mobile) */
.container {
  padding: 16px;
  grid-template-columns: 1fr;
}

/* Tablet: 768px - 1023px */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    grid-template-columns: repeat(4, 1fr);
    max-width: 1400px;
    margin: 0 auto;
  }
}

/* Large Desktop: 1536px+ */
@media (min-width: 1536px) {
  .container {
    max-width: 1600px;
  }
}
```

### Mobile Optimizations
- **Hamburger Menu**: Collapse navigation on mobile
- **Touch Targets**: Minimum 44x44px for tappable elements
- **Bottom Navigation**: Primary actions at thumb reach
- **Swipe Gestures**: Swipe to dismiss modals
- **Reduced Complexity**: Simplify tables to cards on mobile

---

## Animation & Transitions

### Timing Functions
```css
/* Default easing */
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

/* Ease out (elements entering) */
transition-timing-function: cubic-bezier(0, 0, 0.2, 1);

/* Ease in (elements exiting) */
transition-timing-function: cubic-bezier(0.4, 0, 1, 1);
```

### Duration
```css
Fast: 150ms (hover, focus)
Medium: 300ms (transitions, fades)
Slow: 500ms (page transitions)
```

### Common Animations
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale In */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Usage
- **Modals**: Fade in overlay (300ms), scale in modal (300ms)
- **Toasts**: Slide up from bottom (300ms)
- **Dropdowns**: Fade + slide down (150ms)
- **Page Transitions**: Fade (300ms)
- **Loading**: Spin animation (1000ms infinite)

---

## Accessibility (WCAG 2.1 AA)

### Color Contrast
```
Minimum Ratios:
- Normal text (16px): 4.5:1
- Large text (24px): 3:1
- UI components: 3:1

Examples:
✓ Black (#111827) on White (#ffffff): 16.4:1
✓ Blue-600 (#2563eb) on White: 4.6:1
✗ Gray-400 (#9ca3af) on White: 2.8:1 (fails)
```

### Focus Indicators
```css
:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Or custom ring */
:focus-visible {
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}
```

### Keyboard Navigation
- **Tab**: Navigate forward
- **Shift + Tab**: Navigate backward
- **Enter/Space**: Activate buttons
- **Escape**: Close modals/dropdowns
- **Arrow Keys**: Navigate lists/menus

### Screen Reader Support
```html
<!-- Proper labeling -->
<button aria-label="Close modal">×</button>

<!-- Loading states -->
<div role="status" aria-live="polite">
  Loading equipment data...
</div>

<!-- Required fields -->
<input type="text" aria-required="true" />

<!-- Error messages -->
<input aria-describedby="error-msg" aria-invalid="true" />
<span id="error-msg">Serial number is required</span>
```

### Skip Links
```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>
```

---

## Performance Guidelines

### Loading States
```html
<!-- Skeleton loader -->
<div class="skeleton">
  <div class="skeleton-header"></div>
  <div class="skeleton-text"></div>
  <div class="skeleton-text"></div>
</div>

<!-- Spinner -->
<div class="spinner" role="status">
  <span class="sr-only">Loading...</span>
</div>

<!-- Progress bar -->
<div class="progress-bar">
  <div class="progress-fill" style="width: 65%"></div>
</div>
```

### Optimistic UI
- Show success immediately
- Revert if API fails
- Example: Check checkbox → API call in background

### Lazy Loading
- Images: Load when near viewport
- Heavy components: Code split
- Tables: Paginate, don't load all

---

## Error Handling

### Error Message Guidelines
```
❌ Bad: "Error 500"
✅ Good: "Unable to save cleaning log. Please try again."

❌ Bad: "Invalid input"
✅ Good: "Serial number must be at least 3 characters"

❌ Bad: "Failed"
✅ Good: "Photo upload failed. Check your connection and try again."
```

### Error Display
```html
<!-- Inline error -->
<input type="text" aria-invalid="true" />
<p class="error-message">This field is required</p>

<!-- Toast error -->
<div class="toast toast-error">
  <svg>❌</svg>
  <span>Failed to delete equipment</span>
  <button>×</button>
</div>

<!-- Page-level error -->
<div class="alert alert-danger">
  <h3>Unable to load data</h3>
  <p>Check your connection and refresh the page</p>
  <button>Retry</button>
</div>
```

---

## Writing Style Guide

### Voice & Tone
- **Professional but friendly**
- **Clear and concise**
- **Action-oriented**
- **Empathetic to user stress**

### Examples
```
❌ "The system has detected a non-compliance event"
✅ "Cleaning is overdue for Ventilator Unit A"

❌ "Unauthorized access denied"
✅ "You don't have permission to edit this equipment"

❌ "Process completed successfully"
✅ "Cleaning log saved ✓"
```

### Button Text
```
✅ "Log Cleaning" (not "Submit")
✅ "Save Changes" (not "OK")
✅ "Delete Equipment" (not "Confirm")
✅ "Generate Report" (not "Click Here")
```

---

## Mobile-Specific Guidelines

### Touch Targets
- Minimum: 44x44px
- Preferred: 48x48px
- Spacing: 8px minimum between targets

### Mobile Navigation
```
Bottom Tab Bar (Technician View):
┌────┬────┬────┬────┐
│Home│Logs│Alert│ Me │
└────┴────┴────┴────┘
```

### Mobile Forms
- One column layout
- Large input fields (48px height)
- Native keyboards (type="email", type="tel")
- Autocomplete where possible

### Mobile Gestures
- Swipe right: Go back
- Swipe left: Next item
- Pull down: Refresh
- Long press: Context menu

---

## Design Checklist

### Before Launch
- [ ] All colors pass WCAG AA contrast
- [ ] Focus states visible on all interactive elements
- [ ] Forms have clear labels and error messages
- [ ] Buttons have clear, action-oriented text
- [ ] Loading states for async operations
- [ ] Empty states with helpful guidance
- [ ] Error states with recovery actions
- [ ] Success confirmations for important actions
- [ ] Responsive on mobile, tablet, desktop
- [ ] Keyboard navigation works throughout
- [ ] Screen reader tested
- [ ] Images have alt text
- [ ] Forms have proper ARIA labels

---

## Tools & Resources

### Design
- **Figma**: Primary design tool
- **Tailwind CSS**: CSS framework
- **Heroicons**: Icon library
- **Google Fonts**: Typography (if needed)

### Testing
- **Lighthouse**: Performance & accessibility
- **WAVE**: Accessibility scanner
- **Contrast Checker**: Color contrast validation
- **BrowserStack**: Cross-browser testing

### Prototyping
- **Figma Prototypes**: Interactive flows
- **UsabilityHub**: First-click testing
- **Loom**: Demo videos

---

These guidelines ensure CleanTrack maintains a consistent, accessible, and professional user experience across all touchpoints.
