/*
 * @Author: ljx li.junxian@outlook.com
 * @Date: 2023-10-17 18:42:01
 * @LastEditors: ljx li.junxian@outlook.com
 * @LastEditTime: 2023-10-17 20:11:30
 * @FilePath: \2023aut-y2s\FOTCS\02_下推自动机\PushdownAutomaton.java
 * @Description: 
 * 
 * Copyright (c) 2023 by Jx L, All Rights Reserved. 
 */
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;
import java.util.Stack;

public class PushdownAutomaton {

    private Set<Character> inputAlphabet;
    private Set<Character> stackAlphabet;

    public PushdownAutomaton() {
        inputAlphabet = new HashSet<>();
        stackAlphabet = new HashSet<>();
        // Define input alphabet
        inputAlphabet.add('a');
        inputAlphabet.add('b');
        inputAlphabet.add('c');

        // Define stack alphabet
        stackAlphabet.add('b');
        stackAlphabet.add('c');
    }

    public boolean isBalancedBCString(String input) {
        Stack<Character> stack = new Stack<>();
        Set<Character> unrecognizedChars = new HashSet<>();

        for (char ch : input.toCharArray()) {
            if (!inputAlphabet.contains(ch)) {
                unrecognizedChars.add(ch);
                break;  // Break on encountering an unrecognized character
            }
            if (!stackAlphabet.contains(ch)) {
                continue;
            }

            if (stack.isEmpty()) {
                stack.push(ch);
            } else if (stack.peek() == 'b' && ch == 'c') {
                stack.pop();
            } else if (stack.peek() == 'c' && ch == 'b') {
                stack.pop();
            } else {
                stack.push(ch);
            }
        }

        if (!unrecognizedChars.isEmpty()) {
            System.out.println("Invalid character(s) detected: " + unrecognizedChars);
            return false;
        }

        return stack.isEmpty();
    }

    public static void main(String[] args) {
        BalancedBCStringChecker checker = new BalancedBCStringChecker();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("Enter a string to match (type '###' to exit the program): ");
            String inputString = scanner.nextLine().trim();

            if (inputString.equals("###")) {
                break;
            } else {
                boolean isAccepted = checker.isBalancedBCString(inputString);
                System.out.println("String \"" + inputString + "\" is " + (isAccepted ? "accepted" : "not accepted") + "\n");
            }
        }

        scanner.close();
    }
}
