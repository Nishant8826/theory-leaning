# Angular Material

## What is it?
Angular Material is the official UI component library developed and maintained by the Angular team at Google. It implements Google's **Material Design** specifications, providing a rich suite of pre-built, accessible, responsive, and customizable UI components (such as data tables, dialog modals, form fields, navigation sidebars, and menus).

## Why do we need it?
Building complex UI widgets from scratch in pure HTML and CSS—such as accessible modal dialogs, paginated and sortable data tables, or keyboard-navigable dropdowns—is time-consuming and difficult. Developers must manually manage ARIA accessibility tags, keyboard focus trapping, and responsive layouts. 

Angular Material provides battle-tested, fully accessible (a11y) components out of the box, allowing developers to focus directly on core application logic.

```
Building Custom UI From Scratch:
Write custom layout ──> Write accessible ARIA attributes ──> Implement keyboard trapping ──> Add styling (High effort)

Using Angular Material:
Import MatTableModule ──> Bind data source ──> Accessibility, responsiveness, and styles handled automatically
```

## How does it work?
1. **Component-Level Tree-Shaking**: Standalone components import only the specific Material modules they need (e.g., `MatButtonModule`, `MatTableModule`, `MatDialogModule`), ensuring unused components are tree-shaken out of the production bundle.
2. **Theming with SASS**: Configurable SASS mixins allow developers to customize brand color palettes, dark modes, typography, and density across the application.
3. **Angular CDK (Component Development Kit)**: Powers Material components behind the scenes with headless UI primitives—providing accessibility helpers, virtual scrolling, drag-and-drop, and overlay positioning.

## Impact
* **Application Architecture**: Accelerates development velocity with a standardized, consistent design system.
* **Performance**: Granular component modules ensure minimal JavaScript overhead in production builds.
* **Maintainability**: Centralized SASS theme configurations make global styling updates effortless and consistent.

## Real World Example
In an enterprise admin dashboard, developers use `MatTable`, `MatSort`, and `MatPaginator` to render thousands of database records with sorting, pagination, and accessibility controls configured in just a few lines of template code.

## Syntax
* **Installing Angular Material**: `ng add @angular/material`
* **Importing a Component Module**:
```typescript
import { MatButtonModule } from '@angular/material/button';
```
* **Template Usage**: `<button mat-raised-button color="primary">Save Changes</button>`

## Code Examples
Below is a complete implementation demonstrating an interactive Angular Material data table and a modal confirmation dialog:

```typescript
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

export interface UserElement {
  id: number;
  name: string;
  role: string;
}

const USER_DATA: UserElement[] = [
  { id: 1, name: 'Alex Developer', role: 'Solutions Architect' },
  { id: 2, name: 'Sarah Connor', role: 'Frontend Engineer' },
  { id: 3, name: 'John Doe', role: 'Product Designer' }
];

// 1. Reusable Dialog Modal Component
@Component({
  selector: 'app-user-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Confirm Action</h2>
    <mat-dialog-content>
      Are you sure you want to update the directory settings?
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="close(false)">Cancel</button>
      <button mat-raised-button color="warn" (click)="close(true)">Confirm</button>
    </mat-dialog-actions>
  `
})
export class UserDialogComponent {
  private dialogRef = inject(MatDialogRef<UserDialogComponent>);

  close(confirm: boolean): void {
    this.dialogRef.close(confirm);
  }
}

// 2. Main Material Table & Dialog Host Component
@Component({
  selector: 'app-material-demo',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatDialogModule],
  template: `
    <div class="material-container">
      <h3>Active Team Directory</h3>
      
      <table mat-table [dataSource]="dataSource" class="mat-elevation-z2">
        <!-- ID Column -->
        <ng-container matColumnDef="id">
          <th mat-header-cell *matHeaderCellDef> ID </th>
          <td mat-cell *matCellDef="let element"> {{element.id}} </td>
        </ng-container>

        <!-- Name Column -->
        <ng-container matColumnDef="name">
          <th mat-header-cell *matHeaderCellDef> Name </th>
          <td mat-cell *matCellDef="let element"> {{element.name}} </td>
        </ng-container>

        <!-- Role Column -->
        <ng-container matColumnDef="role">
          <th mat-header-cell *matHeaderCellDef> Role </th>
          <td mat-cell *matCellDef="let element"> {{element.role}} </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;" class="table-row"></tr>
      </table>

      <div class="actions">
        <button mat-raised-button color="primary" (click)="openDialog()">Modify Directory</button>
      </div>
    </div>
  `,
  styles: [`
    .material-container { padding: 24px; font-family: Roboto, sans-serif; }
    table { width: 100%; max-width: 520px; margin-bottom: 20px; }
    .table-row:hover { background-color: #f8fafc; }
    .actions { margin-top: 15px; }
  `]
})
export class MaterialDemoComponent {
  private dialog = inject(MatDialog);

  displayedColumns: string[] = ['id', 'name', 'role'];
  dataSource = USER_DATA;

  openDialog(): void {
    const dialogRef = this.dialog.open(UserDialogComponent, {
      width: '350px'
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('Dialog closed with decision:', result);
    });
  }
}
```

## Best Practices
1. **Manage Dialog State Locally**: Avoid injecting `MatDialogRef` into global state stores. Dialog references are short-lived UI controllers that belong inside local components.
2. **Leverage the Angular CDK**: For custom UI components (like dropdown overlays or drag-and-drop lists) where you want custom design without Material aesthetics, use the headless primitives from `@angular/cdk`.
3. **Use SASS Mixins for Theming**: Customize Angular Material component colors and typography using official SASS theming mixins (`mat.define-theme()`) instead of brute-force CSS overrides with `!important`.

## Common Mistakes
* **Brute-Force CSS Overrides**: Overriding Material internal classes with `::ng-deep` or `!important`. Internal DOM structures can change during major Angular Material version upgrades, breaking fragile CSS selectors.
* **Importing Unused Modules**: Adding entire Material component modules (e.g., `MatAutocompleteModule`) to component `imports` when they are not used in the template, increasing bundle sizes needlessly.

## Interview Questions & Answers
### Q: What is the Angular CDK and how does it relate to Angular Material?
**A**: The Angular Component Development Kit (CDK) is a library of headless UI primitives and behavioral utilities (e.g., overlay positioning, focus trapping, virtual scrolling, drag-and-drop) without any predefined visual styling. Angular Material is built on top of the CDK, adding Google's Material Design visual guidelines.

### Q: How do you pass data into and receive data from an Angular Material Dialog?
**A**: Pass data into the dialog using the `data` configuration property in `dialog.open(MyDialogComponent, { data: { id: 10 } })`, and inject it inside the dialog component using the `MAT_DIALOG_DATA` token. Return data back to the caller by passing a payload to `dialogRef.close(resultPayload)`, which emits to the `afterClosed()` Observable stream.

## Summary
Angular Material delivers a comprehensive suite of accessible, production-ready UI components built on Google's Material Design principles. Powered by the Angular CDK and customizable SASS themes, it enables rapid development of polished, accessible web interfaces.

---

Previous : [Authentication and Authorization](./19_Authentication_and_Authorization.md) | Index : [Home](./00_index.md) | Next : [Performance Optimization](./21_Performance_Optimization.md)
