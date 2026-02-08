The pseudo plugin can be configured to return fake data for any UUID.
In the data logger configuration file, create a plugin element like the following:

<plugin name="pseudo">
    <schedule>
        <period>30</period>
        <rollover-count>48</rollover-count>
    </schedule>
    <plugin-config>
    </plugin-config>
</plugin>

Inside the <plugin-config> element, list the values you would like to simulate as follows:

<plugin-config>
    <value>
        <!-- Air Temperature -->
        <uuid>a0ce0210-3bbf-11ee-89eb-00e04c400cc5</uuid>
        <min>0.0</min>
        <max>45.0</max>
    </value>
    <value>
        <!-- Humidity -->
        <uuid>a0ce0211-3bbf-11ee-89eb-00e04c400cc5</uuid>
        <min>60.0</min>
        <max>90.0</max>
    </value>
    <value>
        <!-- Air Pressure -->
        <uuid>a0ce0212-3bbf-11ee-89eb-00e04c400cc5</uuid>
        <min>700.0</min>
        <max>800.0</max>
    </value>
    <value>
        <!-- Water Temperature -->
        <uuid>a0ce0216-3bbf-11ee-89eb-00e04c400cc5</uuid>
        <min>700.0</min>
    </value>
</plugin-config>
