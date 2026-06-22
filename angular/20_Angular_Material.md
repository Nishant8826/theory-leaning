# Angular Material

## What is it?
Angular Material is an official UI component library developed by the Angular team. It implements Google's Material Design specification, providing a collection of pre-built, accessible, and themeable UI components (like tables, dialogs, form controls, and navigation bars).

## Why do we need it?
Building accessible, high-performance UI components (like dropdown menus, modal dialogs, and paginated tables) from scratch is time-consuming. You have to handle ARIA accessibility attributes, keyboard navigation, and responsive layouts. Angular Material provides pre-tested, accessible components out of the box, allowing developers to focus on application logic.

```
Development from scratch:
Write custom layout ──> Write accessible HTML/ARIA ──> Implement keyboard controls ──> Add styling (months of effort)

With Angular Material:
Import MatTableModule ──> Bind data source ──> Access, responsiveness, and styles handled automatically
```

## How does it work?
1. **Component Imports**: Standalone components import specific Material modules (like `MatButtonModule` or `MatTableModule`) directly.
2. **Theming (SASS)**: Uses SASS variables and mixins to customize color palettes, typography, and density across components.
3. **Accessibility (A11y)**: Built on the Angular CDK (Component Dev Kit), which provides utilities for focus trapping, keyboard navigation, and screen reader announcements.

## Impact
* **Application Architecture**: Accelerates UI development by providing standard components.
* **Performance**: Modular design allows you to import only the components you need, keeping bundle sizes small.
* **Maintainability**: Centralizes design rules and styles using Material's theming system.

## Real World Example
An enterprise application uses Angular Material's `MatTable` and `MatPaginator` to render lists of transactions. Users can sort columns and navigate pages, and the table dynamically adapts to mobile screens.

## Syntax
* **Adding Angular Material**: `ng add @angular/material`
* **Importing Material Component**:
```typescript
import { MatButtonModule } from '@angular/material/button';
```
* **Declaring Button**: `<button mat-raised-button color="primary">Click Me</button>`

## Hinglish Explanation

Angular Material Google ki **Material Design** specifications par bani ek popular component library hai. Iska use karke hume tables, sidebars, buttons ya input forms scratch se khud develop aur style nahi karne padte, balki ready-made components use karne ko milte hain.

### 1. Modularity (Har tool alag hai)
* Angular Material me har component (e.g. Table, Button, Dialog) ke module alag hote hain. Aapko poori library ek sath compile karne ke bajaye sirf unhi modules ko import karna chahiye jinhe component me actual use karna ho (jaise `MatTableModule`).

### 2. CDK (Component Dev Kit - Dimaag bina Body ke)
* CDK Angular Material ki foundation hai. Yeh components ke behaviors ko control karti hai (accessibility keyboard shortcuts, focus trapping, overlays) par isme koi default styling/colors nahi hote. Material isi CDK foundation ke upar theme aur Google Material UI add karta hai.

### 3. Theming (Colors setup)
* Material me dynamic color configurations ke liye custom SCSS Mixins use hoti hain. Custom classes me `!important` likh kar styles overwrite karna bad practice hai, hume material ke default themes configuration maps ko dynamic SCSS compile variables se custom theme design karni chahiye.

## Code Examples
Below is an implementation of an Angular Material Dialog modal and a styled Table.

```typescript
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule, MatDialog, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

export interface UserElement {
  id: number;
  name: string;
  role: string;
}

const USER_DATA: UserElement[] = [
  { id: 1, name: 'Nishant', role: 'Architect' },
  { id: 2, name: 'Alice', role: 'Developer' },
  { id: 3, name: 'Bob', role: 'Designer' }
];

// 1. Dialog Component Definition
@Component({
  selector: 'app-user-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Confirm Action</h2>
    <mat-dialog-content>Are you sure you want to modify this user?</mat-dialog-content>
    <mat-dialog-actions>
      <button mat-button (click)="close(false)">Cancel</button>
      <button mat-button color="warn" (click)="close(true)">Confirm</button>
    </mat-dialog-actions>
  `
})
export class UserDialogComponent {
  private dialogRef = inject(MatDialogRef<UserDialogComponent>);

  close(confirm: boolean) {
    this.dialogRef.close(confirm);
  }
}

// 2. Parent Component with Table and Dialog trigger
@Component({
  selector: 'app-material-demo',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatDialogModule],
  template: `
    <div class="material-container">
      <h3>Active Team Directory</h3>
      
      <!-- Material Table -->
      <table mat-table [dataSource]="dataSource" class="mat-elevation-z2">
        <ng-container matColumnDef="id">
          <th mat-header-cell *header-cell-def> ID </th>
          <td mat-cell *mat-cell-def="let element"> {{element.id}} </td>
        </ng-container>

        <ng-container matColumnDef="name">
          <th mat-header-cell *header-cell-def> Name </th>
          <td mat-cell *mat-cell-def="let element"> {{element.name}} </td>
        </ng-container>

        <ng-container matColumnDef="role">
          <th mat-header-cell *header-cell-def> Role </th>
          <td mat-cell *mat-cell-def="let element"> {{element.role}} </td>
        </ng-container>

        <tr mat-header-row *mat-header-rowDef="displayedColumns"></tr>
        <tr mat-row *mat-rowDef="let row; columns: displayedColumns;" class="table-row"></tr>
      </table>

      <div class="actions">
        <button mat-raised-button color="primary" (click)="openDialog()">Modify Directory</button>
      </div>
    </div>
  `,
  styles: [`
    .material-container { padding: 20px; font-family: Roboto, sans-serif; }
    table { width: 100%; max-width: 500px; margin-bottom: 15px; }
    .table-row:hover { background: #f3f4f6; }
    .actions { margin-top: 15px; }
  `]
})
export class MaterialDemoComponent {
  private dialog = inject(MatDialog);

  displayedColumns: string[] = ['id', 'name', 'role'];
  dataSource = USER_DATA;

  openDialog() {
    const dialogRef = this.dialog.open(UserDialogComponent);

    dialogRef.afterClosed().subscribe(result => {
      console.log('Dialog choice result:', result);
    });
  }
}
```
## Best Practices
1. **Avoid Storing Dialog States Globally**: Keep modal dialog lifecycle configurations isolated. Do not expose `MatDialogRef` logic to global state stores.
2. **Leverage the Angular CDK**: If you need a custom UI layout that doesn't follow Material Design guidelines, use the Angular CDK directly. This allows you to build accessible custom components with less styling override overhead.
3. **Use SCSS Mixins for Theming**: Customize the appearance of components using Angular Material's SCSS theming mixins instead of writing CSS overrides with `!important`.

## Common Mistakes
* **Writing Custom CSS Overrides**: Overriding Material styles with custom classes and `!important`. This can cause styling issues when upgrading to newer versions of the library.
* **Importing unnecessary modules**: Importing the entire Angular Material library in a single file instead of importing only the specific component modules you need.

## Interview Questions & Answers
### Q: What is the Angular CDK and how does it relate to Angular Material?
**A**: The Angular CDK (Component Dev Kit) is a library that provides tools to build custom UI components (such as overlay services, accessibility utilities, drag-and-drop tools, and virtual scrolling) without imposing Material Design styling choices. Angular Material is built on top of the CDK.
* **Hinglish Explanation**: Angular CDK (Component Dev Kit) ek core logic library hai jo custom components banane ke liye basic behaviours aur functionalities (jaise accessibility, overlay windows, drag-and-drop, virtual scrolling) provide karti hai bina kisi design style (like colors/themes) ko force kiye. Angular Material is CDK par hi build kiya gaya hai, jo is basic logic ko Google ke Material Design specification ke theme aur elements (styling) me transform karta hai.

### Q: How do you pass data into an Angular Material Dialog?
**A**: Pass data in the configuration object when opening the dialog using the `data` property. For example: `this.dialog.open(MyDialog, { data: { id: 1 } })`. You can then inject this data in the dialog component constructor using the `MAT_DIALOG_DATA` token.
* **Hinglish Explanation**: Dialog kholte waqt configuration object ke under `data` property ka use karke data pass kiya jata hai: `dialog.open(MyDialogComponent, { data: { id: 10 } })`. Phir child dialog component ke constructor me `MAT_DIALOG_DATA` injection token ka use karke use read kiya jata hai: `constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}`.

## Summary
Angular Material implements Google's Material Design specification for Angular. Importing components directly into standalone structures simplifies building accessible, themeable web interfaces.

---

Previous : [Authentication and Authorization](./19_Authentication_and_Authorization.md) | Index : [Home](./00_index.md) | Next : [Performance Optimization](./21_Performance_Optimization.md)
