import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;

// Class representing a single expense
class Expense {
    private String category;
    private double amount;
    private String date;

    public Expense(String category, double amount, String date) {
        this.category = category;
        this.amount = amount;
        this.date = date;
    }

    @Override
    public String toString() {
        return "Category: " + category + ", Amount: $" + amount + ", Date: " + date;
    }
}

// Main class for the GUI
public class ExpenseTrackerGUI extends JFrame {
    private ArrayList<Expense> expenses;
    private DefaultListModel<String> listModel;
    private JList<String> expenseList;

    public ExpenseTrackerGUI() {
        expenses = new ArrayList<>();
        listModel = new DefaultListModel<>();

        // Setup JFrame
        setTitle("Expense Tracker");
        setSize(400, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Header label
        JLabel header = new JLabel("Expense Tracker", SwingConstants.CENTER);
        header.setFont(new Font("Arial", Font.BOLD, 20));
        add(header, BorderLayout.NORTH);

        // Center panel to display expenses
        expenseList = new JList<>(listModel);
        JScrollPane scrollPane = new JScrollPane(expenseList);
        add(scrollPane, BorderLayout.CENTER);

        // Buttons panel
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout());

        JButton addButton = new JButton("Add Expense");
        JButton deleteButton = new JButton("Delete Expense");

        buttonPanel.add(addButton);
        buttonPanel.add(deleteButton);
        add(buttonPanel, BorderLayout.SOUTH);

        // Add Expense Button Action
        addButton.addActionListener(e -> addExpenseDialog());

        // Delete Expense Button Action
        deleteButton.addActionListener(e -> deleteSelectedExpense());

        // Show the window
        setVisible(true);
    }

    private void addExpenseDialog() {
        JTextField categoryField = new JTextField();
        JTextField amountField = new JTextField();
        JTextField dateField = new JTextField();

        Object[] fields = {
            "Category:", categoryField,
            "Amount:", amountField,
            "Date (YYYY-MM-DD):", dateField
        };

        int option = JOptionPane.showConfirmDialog(this, fields, "Add Expense", JOptionPane.OK_CANCEL_OPTION);

        if (option == JOptionPane.OK_OPTION) {
            String category = categoryField.getText();
            double amount;
            String date = dateField.getText();

            try {
                amount = Double.parseDouble(amountField.getText());

                if (!date.matches("\\d{4}-\\d{2}-\\d{2}")) {
                    throw new IllegalArgumentException("Invalid date format.");
                }

                Expense expense = new Expense(category, amount, date);
                expenses.add(expense);
                listModel.addElement(expense.toString());
                JOptionPane.showMessageDialog(this, "Expense added successfully!");
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Invalid input: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void deleteSelectedExpense() {
        int selectedIndex = expenseList.getSelectedIndex();
        if (selectedIndex != -1) {
            expenses.remove(selectedIndex);
            listModel.remove(selectedIndex);
            JOptionPane.showMessageDialog(this, "Expense deleted successfully!");
        } else {
            JOptionPane.showMessageDialog(this, "No expense selected.", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        new ExpenseTrackerGUI();
    }
}