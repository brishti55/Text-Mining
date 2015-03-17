data_DIR = "/Users/Brishti/Documents/Spring 2015 Clasees/Text Mining/Assignment1/Assignment1_Data/"
output_DIR = "/Users/Brishti/Documents/Spring 2015 Clasees/Text Mining/Assignment1/Output/"
output_file_Name = output_DIR + "org_award.txt"
output_abstract_dir = "/Users/Brishti/Documents/Spring 2015 Clasees/Text Mining/Assignment1/Output/Abstract_output/"

$org_award_File = File.open( output_file_Name,"w" )

year = ["1990", "1991", "1992", "1993", "1994"]

line_distribution = Array.new(100,0)

for y in year
  award_DIR = "awards_" + y
  award_Folder_Prefix = "awd_" + y + "_"

  award_Folder_Max = 96

  for id in 0...award_Folder_Max
    award_Folder_Index = sprintf("%02d", id)
    file_Format = ".txt"

    folder_Name=data_DIR + award_DIR + "/" + award_Folder_Prefix + award_Folder_Index + "/"

    #puts folder_Name

    files = Dir[folder_Name + "*" + file_Format]
    if files.size != 0
      for file_Name in files
        puts file_Name
        $nsf_org = ""
        $abstract_identity = ""
        $award_amount = ""
        $abstract = ""
        $will_take_abstract = false
        File.open(file_Name, 'r') do |f1|
          while line = f1.gets
            #puts line
            words=line.force_encoding('iso-8859-1').split(" ")
            #puts words[index]

            if words[0] == "NSF" && words[1] == "Org"
              for index in 3...words.size
                 $nsf_org = $nsf_org + words[index]
                 #puts $nsf_org
              end
            elsif words[0] == "File"
              for index in 2...words.size
                $abstract_identity = words[index]
                #puts $abstract_identity
              end
            elsif words[0] == "Total" && words[1] == "Amt."
                award = words[3]
                tmp= award.split("$")
                $award_amount = tmp[1]
                #puts $award_amount
            elsif words[0] == "Abstract"
              $will_take_abstract = true
            elsif $will_take_abstract == true
              line_words = line.split(" ")
              line_new = line_words.join(" ")
              $abstract = $abstract + line_new + " "
            end
          end
          
          output_abstract_file = File.open(output_abstract_dir + $abstract_identity.to_s + ".txt", "w")
          lines_in_abstract = $abstract.scan(/[^\.!?]+[\.!?]/).map(&:strip)
          line_number = lines_in_abstract.size
          
          check = $abstract.split(" ")
          if check[0] == "Not" && check[1] == "Available"
            line_number = 0
          else
            puts $abstract
          end
          
          puts line_number
      
          line_num = 0
          for j in 0...line_number-1
            tmps = lines_in_abstract[j].split(" ")
            if tmps != "" || tmps != "***" || tmps != "***//" || tmps != "***" || tmps != "."
              s = $abstract_identity + "|" + (j + 1).to_s + "|" + lines_in_abstract[j] + ".\n" 
              output_abstract_file << s
              line_num += 1
            end
          end
          
          line_number = line_num
          line_distribution[line_number] += 1    
          
          #puts " "
          tmp_string = $nsf_org + " " + $award_amount + "\n"
          $org_award_File << tmp_string
        end
      end
    end
  end
end
$org_award_File.close

line_distribution_file = File.open(output_DIR + "line_distribution.txt", "w")

for i in 0...line_distribution.size
  s = i.to_s + " " + line_distribution[i].to_s + "\n"
  line_distribution_file << s
end

org_array = []
#puts output_file_Name
File.open(output_file_Name, "r") do |f2|
  while line = f2.gets
    #puts line
    words=line.force_encoding('iso-8859-1').split(" ")

    if words.size == 1
      next
    end

    org_exists = false

    for org in org_array
      if org == words[0]
        org_exists = true
      end
    end

    if org_exists == false
      org_array.push(words[0])
    end
  end
end

#puts org_array
#puts org_array.size

number_of_org = org_array.size
org_award_count = Array.new(number_of_org, 0)
org_award_total = Array.new(number_of_org, 0)

File.open(output_file_Name, "r") do |f2|
  while line = f2.gets
    #puts line
    words=line.force_encoding('iso-8859-1').split(" ")

    if words.size == 1
      next
    end

    org = words[0]
    award_value = words[1].to_i

    for i in 0...number_of_org
      if org == org_array[i]
        org_award_count[i] += 1
        org_award_total[i] += award_value
      end
    end
  end
end


output_org_award_count_total = File.open(output_DIR + "org_award_count_total.txt", "w")
for i in 0...number_of_org
  output_org_award_count_total << org_array[i] + " " + org_award_count[i].to_s + " " + org_award_total[i].to_s + "\n"
end