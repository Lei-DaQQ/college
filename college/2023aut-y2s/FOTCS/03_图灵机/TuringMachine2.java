
/*
 * @Author: ljx li.junxian@outlook.com
 * @Date: 2023-11-02 09:51:55
 * @LastEditors: ljx li.junxian@outlook.com
 * @LastEditTime: 2023-11-02 13:03:30
 * @FilePath: \03_Í¼Áé»ú\TuringMachine2.java
 * @Description: 
 * 
 * Copyright (c) 2023 by Jx L, All Rights Reserved. 
 */
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class TuringMachine2 {
    private static Map<Character, Integer> symbol = new HashMap<>();
    private static int[][] stateTrans = new int[10][6];
    private static int[][] operation = new int[10][6];

    private static final int Start = 0, S0 = 1, S1 = 2, S2 = 3, S3 = 4, S4 = 5, S5 = 6, S6 = 7, S7 = 8, S8 = 9,
            ACCEPT = 10, REJECT = 11;
    private static final int L = 0, L_x = 1, R = 2, R_x = 3, NA = 4;
    private static Character endCharacter = '$', basCharacter = 'b', delCharacter = 'x';
    private static String indicateCharacter="*";
    static {
        symbol.put(basCharacter, 0);
        symbol.put('#', 1);
        symbol.put('+', 2);
        symbol.put('=', 3);
        symbol.put(delCharacter, 4);
        symbol.put(endCharacter, 5);

        // Define state transitions as integer constants
        stateTrans[0] = new int[] { REJECT, S0, REJECT, REJECT, REJECT, REJECT };
        stateTrans[1] = new int[] { S0, REJECT, S1, REJECT, REJECT, REJECT };
        stateTrans[2] = new int[] { S1, REJECT, REJECT, S2, REJECT, REJECT };
        stateTrans[3] = new int[] { S2, REJECT, REJECT, REJECT, REJECT, S8 };
        stateTrans[4] = new int[] { REJECT, S4, REJECT, REJECT, REJECT, REJECT };
        stateTrans[5] = new int[] { S5, REJECT, S4, S6, S4, REJECT };
        stateTrans[6] = new int[] { S5, REJECT, S5, S7, REJECT, REJECT };
        stateTrans[7] = new int[] { REJECT, REJECT, REJECT, REJECT, S6, ACCEPT };
        stateTrans[8] = new int[] { S8, REJECT, REJECT, REJECT, S7, REJECT };
        stateTrans[9] = new int[] { S8, S3, S8, S8, S8, S8 };

        // Define operation codes as integer constants
        operation[0] = new int[] { NA, R, NA, NA, NA, NA };
        operation[1] = new int[] { R, NA, R, NA, NA, NA };
        operation[2] = new int[] { R, NA, NA, R, NA, NA };
        operation[3] = new int[] { R, NA, NA, NA, NA, L };
        operation[4] = new int[] { NA, R, NA, NA, NA, NA };
        operation[5] = new int[] { R_x, NA, R, R, R, NA };
        operation[6] = new int[] { R, NA, R, R, NA, NA };
        operation[7] = new int[] { NA, NA, NA, NA, R, R };
        operation[8] = new int[] { R_x, NA, NA, NA, R, NA };
        operation[9] = new int[] { L, L, L, L, L, L };
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("This Turing machine recognizes strings of the form '#@^n+@^m=@^k, n+m=k' "); 
        System.out.print("The default symbol for '@' is 'b'. ");
        System.out.println("For example: #bb+b=bbb will accept,  #b+b=bbb will reject.");
        System.out.println("If you want to change the symbol, please enter a character. If you don't want to change, press Enter to continue with 'b'.");
        String input = scanner.nextLine();
    
        if (input.length() == 1 && Character.isLetter(input.charAt(0))) {
            symbol.remove(basCharacter);
            basCharacter = input.charAt(0);
            symbol.put(basCharacter, 0);
            System.out.println("Symbol has been changed to: " + basCharacter);
        } else if (input.length() > 1) {
            System.out.println("Invalid input. Symbol 'b' remains unchanged.");
        }

        

        while (true) {
            System.out.println("\n\nEnter the symbol string to recognize ('###' to exit): ");
            String line = scanner.nextLine();

            if (line.equals("###")) {
                System.out.println("Exiting the program.");
                break;
            }

            line += endCharacter;

            System.out.println("Adding '$' at the end of the string to represent the end marker.");
            System.out.println(
                    "The Turing Machine will print each step, using '"+indicateCharacter+"' to indicate the current scanned position.");
            System.out.println("The Processed Tape: " + line);


            int currentState = Start;
            int idx = 0;

            while (currentState != ACCEPT && currentState != REJECT) {
                System.out.print("Current state: " + currentState);
                System.out.print(", Tape:");
                for (int i = 0; i < line.length(); i++) {
                    if (i != idx) {
                        System.out.print(line.charAt(i));
                    } else {
                        System.out.print( indicateCharacter + line.charAt(i));
                    }
                }
                System.out.print(", Symbol: " + line.charAt(idx));

                int preState = currentState;
                if(symbol.get(line.charAt(idx)) == null){
                    System.out.println(", Invalid symbol!");
                    break;
                }
                currentState = stateTrans[currentState][symbol.get(line.charAt(idx))];
                System.out.print(", Transition to state: " + currentState);
                int op = operation[preState][symbol.get(line.charAt(idx))];
                if (op == L) {
                    System.out.print(", Move left");
                } else if (op == L_x) {
                    System.out.print(", Change symbol to '" + delCharacter + "' and move left");
                } else if (op == R) {
                    System.out.print(", Move right");
                } else if (op == R_x) {
                    System.out.print(", Change symbol to '" + delCharacter + "' and move right");
                }
                System.out.println(" -> ");

                if (op == R_x || op == L_x) {
                    char[] lineChars = line.toCharArray();
                    lineChars[idx] = delCharacter;
                    line = new String(lineChars);
                }
                if (op == L || op == L_x) {
                    idx--;
                }
                if (op == R || op == R_x) {
                    idx++;
                }

                if (idx == -1)
                    idx++;

            }

            if (currentState == ACCEPT) {
                System.out.println("Accept!");
            } else {
                System.out.println("Reject!");
            }
        }
    }// main
}
/*
 * 
 * #b+b=bb
 * 
 */